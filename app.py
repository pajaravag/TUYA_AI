
import sys
import os
import warnings
warnings.filterwarnings("ignore")

from dotenv import load_dotenv
load_dotenv('.env')
MODEL_ID = os.getenv('MODEL_ID')

current_dir = os.path.dirname(os.path.abspath(__file__))

python_code_dir = os.path.join(current_dir, "Python_Code")
sys.path.append(python_code_dir)

print(os.listdir(python_code_dir))

from scraping import Scraper
from Data_Saver import DataSaver
from LLamaQuerier import LlamaQuery

scraper = Scraper(headers = {'User-Agent': 'Mozilla/5.0'})
data_saver = DataSaver()

url_scrape_credit_cards = "https://www.tuya.com.co/tarjetas-de-credito"
url_scrape_credicompras = "https://www.tuya.com.co/credicompras"

scrape_credit_cards_data = scraper.scrape_credit_cards(url_scrape_credit_cards)
scrape_credicompras_data = scraper.scrape_credicompras(url_scrape_credicompras)

data_saver.save_output(scrape_credit_cards_data, "credit_cards")
data_saver.save_output(scrape_credicompras_data, "credicompras")

context_credit_cards = data_saver.upload_contexts("credit_cards")
context_credicompras = data_saver.upload_contexts("credicompras")

llama_query = LlamaQuery(MODEL_ID)

question_1 = "¿Cuáles son los nombres de las tarjetas que tiene disponibles Tuya S.A.?"
question_2 = "¿Cuáles son los valores de la tasa de interés y póliza del producto Credicompras?"

answer_1 = llama_query.ask_llama(question_1, context_credit_cards)
answer_2 = llama_query.ask_llama(question_2, context_credicompras)

data_saver.save_output(answer_1, 'answer_1', 'Output', 'txt')
data_saver.save_output(answer_2, 'answer_2', 'Output', 'txt')

print("✅ All data saved successfully.")
