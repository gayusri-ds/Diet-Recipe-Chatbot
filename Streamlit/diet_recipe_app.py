import streamlit as st
import pandas as pd

# Sample DataFrame (replace with your actual data loading method)
def load_data():
    data = pd.read_excel(r'C:/Users/DELL/Desktop/My Projects/Indian food diet chatbot/diet recipe/cleaned_data.xlsx')
    data.rename(columns={'TranslatedRecipeName': 'RecipeName'}, inplace=True)
    return data

# Function to clean and standardize spacing in text
def clean_whitespace(text):
    return ' '.join(text.split())

# Load data
df = load_data()

# Standardize spacing in recipe names
df['RecipeName'] = df['RecipeName'].apply(clean_whitespace)

# Set display option for full column width
pd.set_option('display.max_colwidth', None)

# Function for chatbot logic
def diet_chatbot(df):
    st.title("🍲 Diet Recipe Chatbot 🥗")
    st.write("Hey there, fellow foodie! I'm your Diet Recipe Chatbot. Let's cook up something delightful together!")

    if 'Diet' not in st.session_state:
        st.write("\nFeeling hungry for something special? Choose your diet type and let's get cooking!", df['Diet'].unique())
        diet_type = st.text_input("Tell me your diet type (e.g., vegetarian, vegan, gluten-free): ", key='diet_type_input').strip().lower()

        if diet_type == 'end':
            st.write("Thank you! Bon appétit, and see you soon!")
            return

        if diet_type in df['Diet'].str.lower().unique():
            st.session_state['Diet'] = diet_type
            df_filtered = df[df['Diet'].str.lower() == diet_type]
        else:
            st.write("Hmmm, I'm not familiar with that diet. Let's try something else!")
            return
    else:
        df_filtered = df[df['Diet'].str.lower() == st.session_state['Diet']]

    if 'Course' not in st.session_state:
        st.write("\nWhat course are you craving? Let's explore our options!", df_filtered['Course'].unique())
        course = st.text_input("Enter your desired course (or type 'back' to go back, 'end' to finish): ", key='course_input').strip().lower()

        if course == 'end':
            st.write("Thank you! Bon appétit, and see you soon!")
            return
        if course == 'back':
            del st.session_state['Diet']
            return

        if course in df_filtered['Course'].str.lower().unique():
            st.session_state['Course'] = course
            df_filtered = df_filtered[df_filtered['Course'].str.lower() == course]
        else:
            st.write("Hmm, not quite what we're serving up today. Let's try another course!")
            return
    else:
        df_filtered = df_filtered[df_filtered['Course'].str.lower() == st.session_state['Course']]

    if 'Cuisine' not in st.session_state:
        st.write("\nLet's spice things up! What cuisine are you in the mood for?", df_filtered['Cuisine'].unique())
        cuisine = st.text_input("Enter your desired cuisine (or type 'back' to go back, 'end' to finish): ", key='cuisine_input').strip().lower()

        if cuisine == 'end':
            st.write("Thank you! Bon appétit, and see you soon!")
            return
        if cuisine == 'back':
            del st.session_state['Course']
            return

        if cuisine in df_filtered['Cuisine'].str.lower().unique():
            st.session_state['Cuisine'] = cuisine
            df_filtered = df_filtered[df_filtered['Cuisine'].str.lower() == cuisine]
        else:
            st.write("Hmm, that's not on the menu today. Let's try another cuisine!")
            return
    else:
        df_filtered = df_filtered[df_filtered['Cuisine'].str.lower() == st.session_state['Cuisine']]

    if 'TotalTimeInMins' not in st.session_state:
        st.write("\nWe're getting closer to mealtime! What's your preferred prep time?", df_filtered['TotalTimeInMins'].unique())
        total_time = st.text_input("Enter your preferred preparation time (in minutes, or type 'back' to go back, 'end' to finish): ", key='total_time_input').strip()

        if total_time == 'end':
            st.write("Thank you! Bon appétit, and see you soon!")
            return
        if total_time == 'back':
            del st.session_state['Cuisine']
            return

        if total_time.isdigit():
            total_time = int(total_time)
            st.session_state['TotalTimeInMins'] = total_time
            df_filtered = df_filtered[df_filtered['TotalTimeInMins'] <= total_time]
        else:
            st.write("Hmmm, I think you forgot to enter a number. Let's try again!")
            return
    else:
        df_filtered = df_filtered[df_filtered['TotalTimeInMins'] <= st.session_state['TotalTimeInMins']]

    if not df_filtered.empty:
        st.write("\nTime to tantalize your taste buds! Here are some recipe options:")
        st.write(df_filtered[['RecipeName', 'PrepTimeInMins', 'CookTimeInMins', 'TotalTimeInMins', 'Servings']])

        chosen_recipe = st.text_input("\nChoose a recipe from the list (or type 'back' to go back, 'end' to finish): ", key='chosen_recipe_input').strip().lower()

        if chosen_recipe == 'end':
            st.write("Thank you! Bon appétit, and see you soon!")
            return
        if chosen_recipe == 'back':
            del st.session_state['TotalTimeInMins']
            return

        # Clean the input recipe name to match standardized recipe names
        cleaned_chosen_recipe = clean_whitespace(chosen_recipe)
        df_filtered['CleanedRecipeName'] = df_filtered['RecipeName'].apply(clean_whitespace)

        if cleaned_chosen_recipe in df_filtered['CleanedRecipeName'].str.lower().values:
            st.session_state['RecipeName'] = cleaned_chosen_recipe
            recipe_details = df_filtered[df_filtered['CleanedRecipeName'].str.lower() == cleaned_chosen_recipe].iloc[0]
        else:
            st.write("Sorry, that dish isn't in our cookbook. Let's pick something else!")
            return
    else:
        st.write("\nLooks like the kitchen's closed for now. Come back later for more tasty treats!")
        return

    # Create the final output DataFrame
    recipe_details_df = pd.DataFrame({
        'Attribute': ['Recipe Name', 'Preparation Time (mins)', 'Cooking Time (mins)', 'Total Time (mins)', 'Servings', 'Ingredients', 'Instructions'],
        'Details': [
            recipe_details['RecipeName'],
            recipe_details['PrepTimeInMins'],
            recipe_details['CookTimeInMins'],
            recipe_details['TotalTimeInMins'],
            recipe_details['Servings'],
            recipe_details['TranslatedIngredients'],
            recipe_details['TranslatedInstructions']
        ]
    })

    # Display selected options as a DataFrame
    selected_df = pd.DataFrame([st.session_state])
    st.write("\nSelected Options:")
    st.write(selected_df)

    # Display recipe details as a two-column DataFrame
    st.write("\nRecipe Details:")
    st.write(recipe_details_df)

    # Display clickable URL
    st.write("\nFor more details, visit the [recipe link]({})".format(recipe_details['URL']))

    st.write("\nGet ready to savor every bite! Happy cooking and happy eating!")

# Streamlit app
if __name__ == "__main__":
    df = load_data()
    diet_chatbot(df)
