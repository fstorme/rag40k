# RAG over Warhammer 40K rules

Small RAG assistant for the Rules of warhammer 40K

# Setup

## Install requirement

Install the requirements :

``pip install -r requirements.txt``

## Download the models

1. Download an embedding model like allMiniLM-L6-v2 from huggingface 
2. Donwload a llm model supported by llamaCPP (I used zephyr-7b-beta.Q3_K_S)
3. Indicate the locations of the moddel in the `streamlit_app.py` script:

    ````
   EMBED_MODEL = <PATH TO YOUR EMBEDING MODEL
   LLM_MODEL = <PATH TO YOUR LLM MODEL>
   ````
# Launch and use the app

run the app with the command 

````
    streamlit run ./rag_rules/app/streamlit_app.py
````

If you run the program locally with limited resources. It can take a few minute to get a result.
Most of the results are of good quality even though it can skip some details.