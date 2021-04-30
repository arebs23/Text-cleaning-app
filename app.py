from altair.vegalite.v4.schema.core import Interpolate
import streamlit as st
import neattext.functions as nfx
import pandas as pd
import re
import spacy
from bs4 import BeautifulSoup
nlp = spacy.load('en_core_web_sm')
from spacy import displacy
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import string

 
def text_analyser(text):
   docx = nlp(text)
   data = [(token.text,token.shape_,token.pos_,token.tag_,token.lemma_,token.is_alpha,token.is_stop) for token in docx]
   df = pd.DataFrame(data,columns = ['TEXT','SHAPE','POS','TAG','LEMMA','ALPHA','STOP'])
   return df

def get_entities(text):
    docx = nlp(text)
    entities = [(entity.text,entity.label_) for entity in docx.ents]
    return entities




##Text downloader
import base64
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

def text_downloader(raw_text):
    b64 = base64.b64encode(raw_text.encode()).decode()
    new_filename = "new_text_file_{}_.txt".format(timestr)
    st.markdown("### **  Download File ###")
    href = f'<a href="data:file/txt;base64,{b64}" download="{new_filename}">Click Here!!</a>'
    st.markdown(href,unsafe_allow_html=True)

def download_csv(data):
    csvfile = data.to_csv(index = False)
    b64 = base64.b64encode(csvfile.encode()).decode()
    new_filename = "new_text_file_{}_.csv".format(timestr)
    st.markdown("### **  Download File ###")
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click Here!!</a>'
    st.markdown(href,unsafe_allow_html=True)


def plot_wordcloud(text):
    my_wordcloud = WordCloud().generate(text)
    fig = plt.figure()
    plt.imshow(my_wordcloud,interpolation = 'bilinear')
    plt.axis('off')
    st.pyplot(fig)

def remove_punctuations(text):
    PUNCT_TO_REMOVE = string.punctuation
    """custom function to remove the punctuation"""
    return text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))


def strip_html_tags(text):
    soup = BeautifulSoup(text,"html.parser")
    [s.extract() for s in soup(['iframe','script'])]
    stripped_text = soup.get_text()
    stripped_text = re.sub(r'[\r|\n|\r\n]+','\n',stripped_text)
    stripped_text = re.sub(r'[\r|\\n|\r\\n]+','\n',stripped_text)
    return stripped_text
    

def remove_mention_tags(text):
    #text = text.str.replace('\n', " ")
    text = re.sub(r"@(\w+)", " ", text)
    text = re.sub(r"#(\w+)", " ", text)
    return text
    


def main():
    st.title("Text cleaner App")

    menu = ["Text cleaner","About"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice =="Text cleaner":
        st.subheader("Text Cleaning")
        text_file = st.file_uploader("Upload txt File",type = ['txt','csv'])
        normalize_case = st.sidebar.checkbox("Normalize case")
        clean_stopwords  = st.sidebar.checkbox("Stopwords")
        clean_punctuation = st.sidebar.checkbox("Punctuation")
        clean_emoji = st.sidebar.checkbox("Emoji")
        clean_mention_tags = st.sidebar.checkbox("Hag Tags")
        remove_urls = st.sidebar.checkbox('Remove Url')
        removel_html = st.sidebar.checkbox("remove_html")
        clean_numbers = st.sidebar.checkbox("Numbers")
        name_entity = st.sidebar.checkbox("Name Entity")

        if text_file is not None:
            raw_text = text_file.read().decode('utf-8')
            file_details = {"Filename":text_file.name,"Filesize":text_file.size,"Filetype":text_file.type}
            st.write(file_details)

            col1,col2 = st.beta_columns(2)

            with col1:
                with st.beta_expander("Original Text"):
                    
                    st.write(raw_text)

            with col2:
                with st.beta_expander("Processed Text"):
                    if normalize_case:
                        raw_text = raw_text.lower()
                    
                    if clean_stopwords:
                        raw_text = nfx.remove_stopwords(raw_text)

                    if clean_numbers:
                        raw_text = nfx.remove_numbers(raw_text)

                    if clean_punctuation:
                        raw_text = remove_punctuations(raw_text)

                    if clean_emoji:
                        raw_text = nfx.remove_emojis(raw_text)
                    
                    if remove_urls:
                        raw_text = nfx.remove_urls(raw_text)

                    if clean_mention_tags:
                        raw_text = remove_mention_tags(raw_text)

                    if name_entity:
                        raw_text = get_entities(raw_text)

                    if removel_html:
                        raw_text = strip_html_tags(raw_text)

                    
                    st.write(raw_text)

                    text_downloader(raw_text)

                
            with st.beta_expander("Textual Analysis"):
                    token_result = text_analyser(raw_text)
                    st.dataframe(token_result)
                    download_csv(token_result)
                    

            
            with st.beta_expander("Plot WOrdcloud"):
                plot_wordcloud(raw_text)

    else:
        st.subheader("About")

if __name__ == '__main__':
    main()