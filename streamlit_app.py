import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Dinner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Soup')
streamlit.text(' 🥗 Salad')
streamlit.text('🥑🍞 Avacado toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# Let's put a pick list here so they can pick the fruit they want to include 
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

def get_fruityadvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  #streamlit.text(fruityvice_response.json())

  # json version of the response and normalize it
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())

  # output the table
  return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
  
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    streamlit.write('The user entered ', fruit_choice)
    back_from_function = get_fruityadvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)    

except URLError as e:
  streamlit.error()

# streamlit.stop()

streamlit.header("The fruit list contains:")
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()
    
#add button to load data
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_row = get_fruit_load_list()
  streamlit.dataframe(my_data_row)

streamlit.header("Want to add fruit to the list")
add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)
def add_to_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("Insert into fruit_load_list values (add_my_fruit)")
    
    return my_cur.fetchall()

if streamlit.button('Load to Fruit Load List'):
  my_add_fruit = add_to_fruit_load_list()
  my_data_row = get_fruit_load_list()
  streamlit.dataframe(my_data_row)
