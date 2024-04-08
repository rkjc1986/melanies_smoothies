# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":cup_with_straw  Customize your Smoothie: :cup_with_straw")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

#import streamlit as st

#title = st.text_input('Movie Title', 'Life of Brian');
#st.write("The current movie title is :", title);

name_on_order  = st.text_input('Name on Smoothie:');
st.write('The name on your smoothie will be : ', name_on_order)


#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect(
    "Choose upto 5 ingredients:",
    my_dataframe,
    max_selections = 5
)

if ingredients_list:
   # st.write(ingredients_list)
   # st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon" + fruit_chosen)
        #st.text(fruityvice_response)    
        fv_df = st.dataframe(data = fruityvice_response.json(), use_container_width= true)
    
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '"""+name_on_order+"""')"""

    st.write(my_insert_stmt)
    #st.stop();
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
      session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered, ' +name_on_order + '!', icon="✅")


    
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response)
fv_df = st.dataframe(data = fruityvice_response.json(), use_container_width= true)
