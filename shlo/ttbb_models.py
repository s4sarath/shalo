import numpy as np
import tensorflow as tf

from collections import defaultdict
from sklearn.decomposition import PCA
from shlo_base import SHLOModel
from utils import scrub, symbol_embedding, SymbolTable


class TTBB(SHLOModel):
    """Implementation of A Simple but Tough-to-Beat-Baseline for Sent. Embedding
    In the basic model, the common component vector is computed before all
    computations. The embeddings are static, so no updates are made.
    """
    def __init__(self, embedding_file, a=0.01, save_file=None, name='TTBB',
                 n_threads=None):
        assert(embedding_file is not None)
        super(TTBB, self).__init__(
            embedding_file, save_file, name, n_threads
        )
        self.a = a

    def _static_common_component(self, tokens, U, p):
        """Compute the common component vector
            @tokens: list of lists of token ids representing sentences
            @U: matrix of word embeddings
            @p: marginal probability estimates for each word
        """
        X = []
        for t in tokens:
            if len(t) == 0:
                X.append(np.zeros(U.shape[1]))
                continue
            # Normalizer
            z = 1.0 / len(t)
            # Embed sentence
            q = (self.a / (self.a + p[t])).reshape((len(t), 1))
            X.append(z * np.sum(q * U[t, :], axis=0))
        # Compute first principal component
        X = np.array(X)
        pca = PCA(n_components=1, whiten=False, svd_solver='randomized')
        pca.fit(X)
        return np.ravel(pca.components_)

    def _preprocess_data(self, sentence_data, init=True):
        # Initialize word table and populate with embeddings
        if init:
            self.word_dict = SymbolTable()
            for word in self.embedding_words:
                self.word_dict.get(word)
        # Process data
        # Just map tokens if not initializing
        if not init:
            return [
                np.ravel([
                    self.word_dict.lookup(scrub(w.lower())) for w in s
                ]) for s in sentence_data
            ]
        # If initializing, get marginal estimates and common component
        marginal_counts = defaultdict(int)
        tokens = []
        for s in sentence_data:
            t = np.ravel([self.word_dict.lookup(scrub(w.lower())) for w in s])
            tokens.append(t)
            for x in t:
                marginal_counts[x] += 1
        # Estimate marginals
        self.marginals = np.zeros(self.word_dict.num_symbols())
        for k, v in marginal_counts.iteritems():
            self.marginals[k] = float(v)
        self.marginals /= sum(marginal_counts.values())
        # Compute sentence embeddings
        self.ccx = self._static_common_component(
            tokens, symbol_embedding(self.embeddings), self.marginals
        )
        self.train_tokens = tokens
        return tokens

    def _get_embedding(self):
        """
        Row 0 is 0 vector for no token
        Row 1 is 0 vector for unknown token
        Remaining rows are constant at pretrained emebdding
        """
        return tf.constant(
            symbol_embedding(self.embeddings),
            dtype=tf.float32, name='embedding_matrix'
        )

    def _get_common_component(self):
        return tf.constant(self.ccx, dtype=tf.float32)

    def _embed_sentences(self):
        """Tensorflow version of @_static_common_component"""
        # Get word features
        word_embeddings = self._get_embedding()
        word_feats      = tf.nn.embedding_lookup(word_embeddings, self.input)
        # Get marginal estimates and scaling term
        batch_size = tf.shape(word_feats)[0]
        p = tf.constant(self.marginals, dtype=tf.float32, name='marginals')
        q = tf.reshape(
            self.a / (self.a + tf.nn.embedding_lookup(p, self.input)),
            (batch_size, self.mx_len, 1)
        )
        # Compute initial sentence embedding
        z = tf.reshape(1.0 / tf.to_float(self.input_lengths), (batch_size, 1))
        S = z * tf.reduce_sum(q * word_feats, axis=1)
        # Common component removal
        ccx = tf.reshape(self._get_common_component(), (1, self.d))
        return S - tf.matmul(S, ccx * tf.transpose(ccx))


class TTBBTune(TTBB):
    """TTBB model with common component updated via gradient descent"""
    def __init__(self, embedding_file, a=0.01, save_file=None, name='TTBBTune',
                 n_threads=None):
        super(TTBBTune, self).__init__(
            embedding_file, a, save_file, name, n_threads
        )

    def _get_embedding(self):
        """
        Row 0 is 0 vector for no token
        Row 1 is 0 vector for unknown token
        Remaining rows are constant at pretrained emebdding
        """
        return tf.Variable(
            symbol_embedding(self.embeddings),
            dtype=tf.float32, name='embedding_matrix'
        )

    def _get_common_component(self):
        return tf.Variable(self.ccx, dtype=tf.float32)


class TTBBTuneLazy(TTBB):
    """TTBB model with exact common component updates
    Common component vector updated after every epoch
    """
    def __init__(self, embedding_file, a=0.01, save_file=None,
                 name='TTBBTuneLazy', n_threads=None):
        super(TTBBTuneLazy, self).__init__(
            embedding_file, a, save_file, name, n_threads
        )

    def _get_feed(self, x_batch, len_batch, y_batch=None):
        feed = {
            self.input:           x_batch, 
            self.input_lengths:   len_batch,
            self.ccx_placeholder: self.ccx,
        }
        if y_batch is not None:
            feed[self.y] = y_batch
        return feed

    def _epoch_post_process(self, t):
        # Update the common component
        U = self.session.run(self.U)
        self.ccx = self._static_common_component(
            self.train_tokens, U, self.marginals
        )

    def _get_embedding(self):
        """
        Row 0 is 0 vector for no token
        Row 1 is 0 vector for unknown token
        Remaining rows are constant at pretrained emebdding
        """
        self.U = tf.Variable(
            symbol_embedding(self.embeddings),
            dtype=tf.float32, name='embedding_matrix'
        )
        return self.U

    def _get_common_component(self):
        self.ccx_placeholder = tf.placeholder(tf.float32, name='common_comp')
        return self.ccx_placeholder