python -u fit_model.py ttbbtuneexact configs/optimal/ttbbtuneexact-imdb.json -embedding data/depw2v.pkl -word_freq data/word_freq.pkl   &> optimal/ttbbtuneexact-imdb.log 
python -u fit_model.py ttbbtuneexact configs/optimal/ttbbtuneexact-agnews.json -embedding data/depw2v.pkl -word_freq data/word_freq.pkl  &> optimal/ttbbtuneexact-agnews.log 
python -u fit_model.py ttbbtuneexact configs/optimal/ttbbtuneexact-amazon.json -embedding data/depw2v.pkl -word_freq data/word_freq.pkl &> optimal/ttbbtuneexact-amazon.log 
python -u fit_model.py ttbbtune configs/optimal/ttbbtune-imdb.json -embedding data/depw2v.pkl -word_freq data/word_freq.pkl   &> optimal/ttbbtune-imdb.log 
python -u fit_model.py ttbbtune configs/optimal/ttbbtune-agnews.json -embedding data/depw2v.pkl -word_freq data/word_freq.pkl  &> optimal/ttbbtune-agnews.log 
python -u fit_model.py ttbbtune configs/optimal/ttbbtune-amazon.json -embedding data/depw2v.pkl -word_freq data/word_freq.pkl &> optimal/ttbbtune-amazon.log 
python -u fit_model.py ttbb configs/optimal/ttbb-imdb.json -embedding data/depw2v.pkl -word_freq data/word_freq.pkl   &> optimal/ttbb-imdb.log 
python -u fit_model.py ttbb configs/optimal/ttbb-agnews.json -embedding data/depw2v.pkl -word_freq data/word_freq.pkl  &> optimal/ttbb-agnews.log 
python -u fit_model.py ttbb configs/optimal/ttbb-amazon.json -embedding data/depw2v.pkl -word_freq data/word_freq.pkl &> optimal/ttbb-amazon.log 

python -u fit_model.py linearmodel configs/optimal/linearmodel-imdb.json -embedding data/depw2v.pkl -word_freq data/word_freq.pkl   &> optimal/linearmodel-imdb.log 
python -u fit_model.py linearmodel configs/optimal/linearmodel-agnews.json -embedding data/depw2v.pkl -word_freq data/word_freq.pkl  &> optimal/linearmodel-agnews.log 
python -u fit_model.py linearmodel configs/optimal/linearmodel-amazon.json -embedding data/depw2v.pkl -word_freq data/word_freq.pkl &> optimal/linearmodel-amazon.log 
python -u fit_model.py sparselm configs/optimal/sparselm-imdb.json -embedding data/depw2v.pkl -word_freq data/word_freq.pkl   &> optimal/sparselm-imdb.log 
python -u fit_model.py sparselm configs/optimal/sparselm-agnews.json -embedding data/depw2v.pkl -word_freq data/word_freq.pkl  &> optimal/sparselm-agnews.log 
python -u fit_model.py sparselm configs/optimal/sparselm-amazon.json -embedding data/depw2v.pkl -word_freq data/word_freq.pkl &> optimal/sparselm-amazon.log 
python -u fit_model.py fasttextpretrain configs/optimal/fasttextpretrain-imdb.json -embedding data/depw2v.pkl -word_freq data/word_freq.pkl   &> optimal/fasttextpretrain-imdb.log 
python -u fit_model.py fasttextpretrain configs/optimal/fasttextpretrain-agnews.json -embedding data/depw2v.pkl -word_freq data/word_freq.pkl  &> optimal/fasttextpretrain-agnews.log 
python -u fit_model.py fasttextpretrain configs/optimal/fasttextpretrain-amazon.json -embedding data/depw2v.pkl -word_freq data/word_freq.pkl &> optimal/fasttextpretrain-amazon.log 
