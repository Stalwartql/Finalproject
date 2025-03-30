import streamlit as st
from auth1 import register, login
import random
import pandas as pd
import time
import qrcode
from datetime import datetime
import io
from unsplashAPI import get_unsplash_image
from hugchat.login import Login
from hugchat import hugchat

# Initialize session state for authentication
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "Home"
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "email" not in st.session_state:
    st.session_state["email"] = ""

# App Configuration
st.set_page_config(page_title="Study Planner", page_icon="📚", layout="wide")

# Custom CSS to style the sidebar
st.markdown("""<style>[data-testid="stSidebar"] {background-color: #ADD8E6; /* Light Blue */}</style>""",
    unsafe_allow_html=True)

@st.cache_resource
def connect_to_hugging_face():
    hf_email = st.secrets['email']
    hf_pass = st.secrets['password']
    # connect to hugging face
    sign = Login(hf_email, hf_pass)
    cookies = sign.login()

    return cookies

# Function to display a back button
def show_back_button():
    if st.button("←"):
        st.session_state["page"] = "Navigation"
        st.rerun()

# Sidebar Navigation
st.sidebar.title("**ZenStudy**")
if st.sidebar.button(" 🏠 **Home** "):
    st.session_state["page"] = "Home"
if st.sidebar.button(" 🗂**Navigation**"):
    st.session_state["page"] = "Navigation"
if st.sidebar.button(" 🔑**Login** "):
    st.session_state["page"] = "Login"
    st.rerun()
# Show 'Your Account' button if the user is logged in
if st.session_state["logged_in"]:
    if st.sidebar.button(" 👤 **Your Account**"):
        st.session_state["page"] = "Your Account"
        st.rerun()

# Render pages based on selection
if st.session_state["page"] == "Home":
    # Create a layout with columns to center the image
    col1, col2, col3 = st.columns([4, 1, 4])  # Adjust column widths for centering
    with col1:
        st.title("**Welcome to ZenStudy** 🌿✏️📚")
        st.write("**Your Personalized Study Planner & Book Explorer App** ✨")
        st.markdown("🔗 Seamless Learning, Effortless Access")
        st.markdown("🎯 Your Learning, Your Way.")
    with col3:
        st.image("./image/planner1.jpg", caption="Boost your learning with ZenStudy", width=500)

    # Read and display the markdown content
    with open("home_text.md", "r", encoding="utf-8") as file:
        home_text = file.read()

    st.markdown(home_text)

elif st.session_state["page"] == "Navigation":
    st.header("Productivity Hub 🚀")
    st.write("Choose a tool and make your study sessions more efficient. Stay on top of your tasks, track progress, and achieve your goals!")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("**Study Planner** 📅"):
            st.session_state["page"] = "Study Planner"
            st.rerun()

    with col2:
        if st.button("**International Book Explorer** 📚"):
            st.session_state["page"] = "International Book Explorer"
            st.rerun()

    with col3:
        if st.button("**Productivity Tracker** 📊"):
            st.session_state["page"] = "Productivity Tracker"
            st.rerun()

    col4, col5 = st.columns(2)

    with col4:
        if st.button("**Pomodoro Timer** ⏳"):
            st.session_state["page"] = "Pomodoro Timer"
            st.rerun()

    with col5:
        if st.button("**QR Code Generator** 🔗"):
            st.session_state["page"] = "QR Code Generator"
            st.rerun()

    # 🎨 Unsplash Image Search Feature
    st.subheader("**Explore Images** 🔍")
    st.write("Find any image you’d like to see! 🌍📸")
    search_query = st.text_input("Enter a keyword:")

    if st.button("Search Image"):
        image_url = get_unsplash_image(search_query)
        if image_url:
            st.image(image_url, caption=f"Image result for: {search_query}", use_container_width=True)
        else:
            st.error("No image found. Try another search!")

    st.subheader("Music 🎶")
    st.write("Boost your mood and focus with music! 🎵")
    with st.expander("Click to Expand"):
        spotify_url = "https://open.spotify.com/embed/playlist/37i9dQZF1DX4sWSpwq3LiO"
        st.markdown(
            f'<iframe src="{spotify_url}" width="100%" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>',
            unsafe_allow_html=True)

    st.subheader("HuggingFace 🤗")
    st.write("Enter a Prompt or Ask Whatever you want to explore")
    def generate_response(prompt):
        cookies = connect_to_hugging_face()
        # Create ChatBot
        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        return chatbot.chat(prompt)

    if st.button("Click to connect to HuggingFace"):
        prompt = st.chat_input("Enter a Prompt or Ask Whatever you want")
        if prompt:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = generate_response(prompt)
                    st.write(response)


elif st.session_state["page"] == "Login":
    show_back_button()
    st.header("🔐Login / Register")
    st.subheader("Join us to have access to more features")
    username = st.text_input("Username", key="username_input")
    email = st.text_input("Email", key="email_input")
    password = st.text_input("Password", type="password", key="password_input")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            user_email = login(username, password)
            if user_email:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["email"] = user_email  # Store email in session
                st.success(f"Welcome, {username}!")
                st.session_state["page"] = "Navigation"  # Redirect after login
                st.rerun()
            else:
                st.error("User not found.")

    with col2:
        if st.button("Register"):
            if username and email and password:
                message = register(username, password, email)
                if "successful" in message:
                    st.success("Thank you for your registration, Now you are a member. You can log in.")
                else:
                    st.error(message)
            else:
                st.warning("Please fill in all fields.")

elif st.session_state["page"] == "Your Account":
    st.header("👤 Your Account")
    st.write(f"**Username:** {st.session_state['username']}")
    st.write(f"**Email:** {st.session_state['email']}")
    st.write(f"**Password:** {'•' * 8}")

    if st.button("Log out"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.session_state["email"] = ""
        st.session_state["page"] = "Home"
        st.rerun()

st.sidebar.warning(" Login to Access QR Code Generator and Productivity Tracker.")

# Feature Pages
if st.session_state["page"] == "Study Planner":
    show_back_button()
    st.title("Study Planner 📅")
    st.subheader("Your Study Planner🤞🏻✨")
    # Initialize session state for task management
    if "tasks" not in st.session_state:
        st.session_state.tasks = []
    st.subheader("📅 Plan Your Study Sessions")
    # Layout: Input form on the left, progress tracking on the right
    col1, col2 = st.columns([3, 2])
    with col1:
        task = st.text_input("Enter Study Task", key="task_input")
        deadline = st.date_input("Deadline", min_value=datetime.today())
        priority = st.selectbox("Priority", ["Low", "Medium", "High"], key="priority_select")
        category = st.selectbox("Category",
                                ["Reading", "Writing", "Coding", "Math", "Science", "Language Learning", "Exercise",
                                 "Other"],
                                key="category_select")
        estimated_time = st.number_input("Estimated Study Time (hours)", min_value=0.5, step=0.5, key="time_input")

        if st.button("➕Add Task", use_container_width=True):
            new_task = {"Task": task, "Deadline": deadline.strftime("%Y-%m-%d"), "Priority": priority,
            "Category": category, "Estimated Time": estimated_time, "Completed": False, "Actual Time": 0}
            st.session_state.tasks.append(new_task)
            st.rerun()  # Ensure tasks update only when a new task is added

    with col2:
        st.subheader("📈Study Progress")
        completed_tasks = sum(1 for t in st.session_state.tasks if t["Completed"])
        total_tasks = len(st.session_state.tasks)
        progress = completed_tasks / total_tasks if total_tasks > 0 else 0
        st.progress(progress)
        st.write(f"**✅ {completed_tasks} / {total_tasks} Tasks Completed**")

    st.subheader("🔔Reminders & Notifications")
    today = datetime.today().date()
    due_soon = [task for task in st.session_state.tasks if
                datetime.strptime(task["Deadline"], "%Y-%m-%d").date() <= today]

    if due_soon:
        st.warning(f"⚠️ You have {len(due_soon)} tasks due today or overdue!")
        for task in due_soon:
            st.write(f"📌 **{task['Task']}** - Due: **{task['Deadline']}** ({task['Priority']} Priority)")

    st.subheader("📝 Your Study Plan")

    if st.session_state.tasks:
        df = pd.DataFrame(st.session_state.tasks)
        # Priority color mapping
        priority_colors = {
            "High": "background-color: #FFCCCC;",  # Light Red
            "Medium": "background-color: #FFF3CD;",  # Light Yellow
            "Low": "background-color: #D4EDDA;"  # Light Green
        }
        styled_df = df.style.map(lambda cell: priority_colors.get(cell, ""), subset=["Priority"])
        # Editable task table with completed checkbox
        edited_df = st.data_editor(df, column_config={"Completed": st.column_config.CheckboxColumn()}, hide_index=True)
        # Update session state with edited values
        for i, task in enumerate(st.session_state.tasks):
            task["Completed"] = edited_df.iloc[i]["Completed"]
    else:
        st.info("No tasks added yet. Start planning!")

elif st.session_state["page"] == "International Book Explorer":
    show_back_button()
    st.title("International Book Explorer 📚")
    st.subheader("Discover the Best Books from Around the World 🌍📖")
    # Sample book data
    books_by_country = {
        "Iran": [
            "Kelidar, Mahmoud Dowlatabadi, 1984",
            "Things We Left Unsaid, Zoya Pirzad, 2001",
            "The Colonel, Mahmoud Dowlatabadi, 2009",
            "Symphony of the Dead, Abbas Maroufi, 1989",
            "Bone of a Pig Hands of a Leper, Mostafa Mastoor, 2014",
            "My Uncle Napoleon, Iraj Pezeshkzad, 1973",
            "Savushun, Simin Daneshvar, 1969",
            "The Blind Owl, Sadesh Hedayat, 1936",
            "Fall is the Last Season of the Year, Nasim Marashi, 2015",
            "Her Eyes, Bozorg Alavi, 1952"],
        "Germany": [
            "All Quiet on the western front, Erich Maria Remarque, 1928",
            "Why we took the car, Wolfgang Herndorf, 2010",
            "The rise and fall of the third reich, William l.Shirer, 1960",
            "Mother courage and her children, Bertolt Brecht, 1941",
            "Buddenbrooks, Thomas Mann, 1901",
            "The sorrows of young werther, Johann Wolfgang von Goethe, 1774",
            "Demaian, Hermann Hesse, 1919",
            "Bricks and mortar, Clemens Meyer, 2016",
            "The swarm, Frank Schätzing, 2004"],
        "Italy": [
            "The name of the rose, Umberto Eco, 1980",
            "If this is a man, Primo Levi, 1947"
            "A room with a view, E.M. Forster, 1908",
            "The decameron, Giovanni Boccaccio, 1999",
            "My brilliant friend, Elena Ferrante, 2011",
            "An Italian in Italy, Beppe Severgnini, 2005",
            "The Baron in the trees, Italo Calvino, 1957",
            "Athread of grace, Mary Doria Russell, 2005",
            "A thousand days in Venice, Marlena de blasi, 2002",
            "The house by the medlar tree, Giovanni Verga, 1881"],
        "United States": [
            "Beloved, Toni Marrison, 1987",
            "Their eyes were watching god, Zora Neale Hurston, 1937",
            "Little woman, Louisa May Alcott, 1868",
            "The grapes of wrath, John Steinbeck, 1939",
            "A tree grows in brooklyn, Betty Smith, 1982",
            "A prayer for owen meany, John Irving, 1989",
            "The color purple, Alice Walker, 1982",
            "Where the red fern grows, Wilson Rawls, 1961",
            "The coldest winter ever, Sister Souljah, 1999",
            "A game of thrones, George R. R Martin, 1996"],
        "Austria": [
            "Radetzky March, Joseph Roth, 1932",
            "The Man Without Qualities, Robert Musil, 1930",
            "The Star of Kazan, Eva Ibbotson, 2004",
            "The World of Yesterday, Stefan Zweig, 1941",
            "The Piano Teacher, Elfriede Jelinek, 1983",
            "Hitler's Vienna, Brigitte Hamann, 1996",
            "Wittgenstein's Nephew, Thomas Bernhard, 1982",
            "The Camera Killer, Thomas Glavinic, 2001",
            "Thunder at Twilight, Frederic Morton, 1989",
            "A Nervous Splendor, Frederic Morton, 1979"],
        "Russia": [
            "War and Peace, Leo Tolstoy, 1869",
            "Fathers and Sons, Ivan Turgenev, 1862",
            "The Brothers Karamazov, Fyodor Dostoevsky, 1880",
            "Oblomov, Ivan Goncharov, 1859",
            "Eugene Onegin, Alexander Pushkin, 1833",
            "The House of the Dead, Fyodor Dostoevsky, 1861",
            "What Is to Be Done?, Nikolay Chernyshevsky, 1863",
            "The Idiot, Fyodor Dostoevsky, 1869",
            "And Quiet Flows the Don, Mikhail Sholokhov, 1928",
            "In the First Circle, Aleksandr Solzhenitsyn, 1968"],
        "France": [
            "The Red and the Black, Stendhal, 1830",
            "The Count of Monte Cristo, Alexandre Dumas, 1844",
            "The Imaginary Invalid, Molière, 1673",
            "The Three Musketeers, Alexandre Dumas, 1844",
            "Froth on the Daydream, Boris Vian, 1947",
            "Bonjour Tristesse, Françoise Sagan, 1954",
            "Bel-ami: The History of a Heart, Guy de Maupassant, 1885",
            "Tartuffe, Molière, 1664",
            "La Fontaine's Fables, Jean de La Fontaine, 1668",
            "Memoirs of Hadrian, Marguerite Yourcenar, 1951"],
        "Netherlands": [
            "The Dinner, Herman Koch, 2009",
            "The Dark Room of Damocles, Willem Frederik Hermans, 1958",
            "The Tea Lords, Hella S. Haasse, 1992",
            "The Assault, Harry Mulisch, 1982",
            "Heart of Stone, Renate Dorrestein, 1998",
            "Grand Hotel Europa, Ilja Leonard Pfeijffer, 2018",
            "The Two Hearts of Kwasi Boachi, Arthur Japin, 1997",
            "The Vanishing, Tim Krabbé, 1984",
            "The Discovery of Heaven, Harry Mulisch, 1992",
            "The Evenings, Gerard Reve, 1947"],
        "Poland": [
            "Solaris, Stanisław Lem, 1961",
            "The Street of Crocodiles, Bruno Schulz, 1934",
            "Ferdydurke, Witold Gombrowicz, 1937",
            "Choucas, Zofia Nałkowska, 1920",
            "This Way for the Gas, Ladies and Gentlemen, Tadeusz Borowski, 1948",
            "Night, Elie Wiesel, 1956",
            "Ashes and Diamonds, Jerzy Andrzejewski, 1948",
            "The Old Axolotl: Hardware Dreams, Jacek Dukaj, 2015",
            "The Beautiful Mrs. Seidenman, Andrzej Szczypiorski, 1943",
            "The Doll, Bolesław Prus, 1889"],
        "Greece": [
            "Gates of Fire, Steven Pressfield, 1998",
            "The Sea of Monsters, Rick Riordan, 2006",
            "Captain Corelli's Mandolin, Louis de Bernières, 1994",
            "Histories, Herodotus, 1830",
            "Fire from Heaven, Mary Renault, 1969",
            "The Song of Achilles, Madeline Miller, 2011",
            "Why I Killed My Best Friend, Amanta Michalopoulou, 2003",
            "Eleni, Nicholas Gage, 1983",
            "The Last Temptation of Christ, Nikos Kazantzakis, 1952",
            "The Magus, John Fowles, 1965"],
        "Ukraine": [
            "The White Guard, Mikhail Bulgakov, 1925",
            "Death and the Penguin, Andrey Kurkov, 1996",
            "Everything is Illuminated, Jonathan Safran Foer, 2002",
            "Life and Fate, Vasily Grossman, 1980",
            "Grey Bees, Andrey Kurkov, 2018",
            "The Moscoviad, Yuri Andrukhovych, 1993",
            "Voroshilovgrad, Serhiy Zhadan, 2010",
            "Mesopotamia, Serhiy Zhadan, 2014",
            "Perversion, Yuri Andrukhovych, 1997",
            "Sweet Darusia, Maria Matios, 2004"],
        "Canada": [
            "Anne of Green Gables, L.M. Montgomery, 1908",
            "Who Do You Think You Are, Alice Munro, 1978",
            "The Handmaid’s Tale, Margaret Atwood, 1985",
            "Stone Diaries, Carol Shields, 1995",
            "Three Day Road, Joseph Boyden, 2005",
            "The Book of Negroes, Lawrence Hill, 2007",
            "Fifth Business, Robertson Davies, 1970",
            "Bear, Marian Engel, 1976",
            "The English Patient, Michael Ondaatje, 1992",
            "Obasan, Joy Kogawa, 1981"],
        "Spain": [
            "A Heart So White, Javier Marías, 1992",
            "The House of the Spirits, Isabel Allende, 1982",
            "Don Quixote, Miguel de Cervantes, 1605",
            "Love in the Time of Cholera, Gabriel García Márquez, 1985",
            "The Bad Girl, Mario Vargas Llosa, 2006",
            "Homeland, Fernando Aramburu, 2016",
            "The Dinner Guest, Gabriela Ybarra, 2015",
            "The Frozen Heart, Almudena Grande, 2007",
            "The Family of Pascual Duarte, Camilo José Cela, 1942"],
        "United Kingdom": [
            "Middlemarch, George Eliot, 1869",
            "To the Lighthouse, Virginia Woolf, 1927",
            "Mrs. Dalloway, Virginia Woolf, 1925",
            "Big Hopes, Charles Dickens, 1861",
            "Jane Eyre, Charlotte Brontë, 1847",
            "Desolate House, Charles Dickens, 1853",
            "Wuthering Heights, Emily Brontë, 1847",
            "Jude the Obscure, Thomas Hardy, 1895",
            "Clarissa, Samuel Richardson, 1747",
            "Heart of Darkness, Joseph Conrad, 1899"],
        "Denmark": [
            "The Danish Girl, David Ebershoff, 2000",
            "Hamlet, William Shakespeare, 1603",
            "The Little Mermaid, Hans Christian Andersen, 1836",
            "Absolution, Olaf Olafsson, 1991",
            "Stolen Spring, Hans Scherfig, 1940",
            "The Spectator Bird, Wallace Stegner, 1976",
            "Copenhagen Connection, Elizabeth Peters, 1982",
            "Number the Stars, Lois Lowry, 1989",
            "Echoland, Per Petterson, 1989",
            "Irretrievable, Theodor Fontane, 1891"],
        "Egypt": [
            "Child of the Morning, Pauline Gedge, 1976",
            "Death on the Nile, Agatha Christie, 1937",
            "Lion in the Valley, Barbara Mertz, 1986",
            "The Map of Love, Ahdaf Soueif, 1999",
            "The White Nile, Alan Moorehead, 1960",
            "In the Eye of the Sun, Ahdaf Soueif, 1992",
            "Sugar Street, Naguib Mahfouz, 1957",
            "Utopia, Ahmed Khaled Tawfik, 2008",
            "Vertigo, Ahmed Mourad, 2007",
            "In the Spider’s Room: A Novel, Mohammed Abdel Nabi, 2017"],
        "Mexico": [
            "The Death of Artemio Cruz, Carlos Fuentes, 1962",
            "Sea Monsters, Chloe Aridjis, 2019",
            "Paradais, Fernanda Melchor, 2021",
            "Hurricane Season, Fernanda Melchor, 2017",
            "Signs Preceding the End of the World, Yuri Herrera, 2019",
            "Umami, Laia Jufresa, 2015",
            "Faces in the Crowd, Valeria Luiselli, 2011",
            "On Lighthouses, Jazmina Barrera, 2020",
            "Ramifications, Daniel Saldaña París, 2018",
            "Pedro Páramo, Juan Rulfo, 1955"],
        "Colombia": [
            "One Hundred Years of Solitude, Gabriel García Márquez, 1967",
            "The Bitch, Pilar Quintana, 2017",
            "Fruit of the Drunken Tree: A Novel, Ingrid Rojas Contreras, 2018",
            "The Armies, Evelio Rosero, 2007",
            "Reputations, Juan Gabriel Vásquez, 2013",
            "Return to the Dark Valley, Santiago Gamboa, 2016",
            "Love in the Time of Cholera, Gabriel García Márquez, 1985",
            "The Dark Bride, Laura Restrepo, 2001",
            "Chronicle of a Death Foretold, Gabriel García Márquez, 1981",
            "Fiebre Tropical, Julián Delgado Lopera, 2020"],
        "Turkey": [
            "The Time Regulation Institute, Ahmet Hamdi Tanpınar, 1954",
            "Snapping Point, Aslı Biçen, 2021",
            "Human Landscapes from My Country, Nâzım Hikmet, 1938",
            "Memed My Hawk, Yaşar Kemal, 1955",
            "Life is a Caravanserai, Emine Sevgi Özdamar, 1992",
            "The Kiss Murder, Mehmet Murat Somer, 2003",
            "Three Daughters of Eve, Elif Shafak, 2016",
            "The Bastard of Istanbul, Elif Shafak, 2006",
            "Portrait Of A Turkish Family, Irfan Orga, 1950",
            "The Girl in the Tree, Şebnem İşigüzel, 2020"],
        "Japan": [
            "The Time Regulation Institute, Ahmet Hamdi Tanpınar, 1954",
            "Snapping Point, Aslı Biçen, 2021",
            "Human Landscapes from My Country, Nâzım Hikmet, 1938",
            "Memed My Hawk, Yaşar Kemal, 1955",
            "Life is a Caravanserai, Emine Sevgi Özdamar, 1992",
            "The Kiss Murder, Mehmet Murat Somer, 2003",
            "Three Daughters of Eve, Elif Shafak, 2016",
            "The Bastard of Istanbul, Elif Shafak, 2006",
            "Portrait Of A Turkish Family, Irfan Orga, 1950",
            "The Girl in the Tree, Şebnem İşigüzel, 2020"]}

    # Title
    st.markdown("<h1 style='color:purple;'>📚 Explore Books by Country</h1>", unsafe_allow_html=True)

    # Country Selection
    selected_country = st.selectbox("Choose a country:", list(books_by_country.keys()))

    # Display Books
    if selected_country:
        st.write(f"### 📖 Books from {selected_country}:")
        for book in books_by_country[selected_country]:
            st.write(f"- {book}")

elif st.session_state["page"] == "Productivity Tracker":
    show_back_button()
    st.title("Productivity Tracker 📊")
    if not st.session_state["logged_in"]:
        st.warning("🔒 Please log in to access this feature.")
    else:
        if st.session_state["logged_in"]:
            st.subheader("Track Your Progress with Charts")

            # Initialize session state for study tracking
            if "study_sessions" not in st.session_state:
                st.session_state.study_sessions = []
            if "study_goal" not in st.session_state:
                st.session_state.study_goal = 10  # Default: 10 hours per week

            st.subheader("🎯 Set Your Study Goal")
            st.session_state.study_goal = st.slider("Weekly Study Goal (Hours)", min_value=5, max_value=40, value=10)
            st.write(f"✅ Your study goal is set to **{st.session_state.study_goal}** hours per week.")

            st.subheader("⏳ Log Your Study Session")
            study_time = st.number_input("How many hours did you study?", min_value=0.5, step=0.5)
            study_date = st.date_input("Select study date")

            if st.button("📌 Add Study Log"):
                st.session_state.study_sessions.append({"Date": study_date.strftime("%Y-%m-%d"), "Hours": study_time})
                st.success("Study session logged successfully!")

            st.subheader("📊 Study Reports")
            df = pd.DataFrame(st.session_state.study_sessions)

            if not df.empty:
                df["Date"] = pd.to_datetime(df["Date"])
                df["Week"] = df["Date"].dt.isocalendar().week
                df["Month"] = df["Date"].dt.month

                report_type = st.radio("View Report", ["Daily", "Weekly", "Monthly"], horizontal=True)

                if report_type == "Daily":
                    daily_report = df.groupby("Date")["Hours"].sum()
                    st.line_chart(daily_report)

                elif report_type == "Weekly":
                    weekly_report = df.groupby("Week")["Hours"].sum()
                    st.bar_chart(weekly_report)

                elif report_type == "Monthly":
                    monthly_report = df.groupby("Month")["Hours"].sum()
                    st.area_chart(monthly_report)
            else:
                st.info("No study sessions logged yet.")

            st.subheader("🏆 Leaderboard & Achievements")
            total_study_hours = sum([s["Hours"] for s in st.session_state.study_sessions])

            if total_study_hours >= st.session_state.study_goal:
                st.success(
                    f"🎉 Congratulations! You've reached your weekly study goal of {st.session_state.study_goal} hours!")

            badges = [("📗 Beginner", 5), ("📘 Intermediate", 10), ("📙 Advanced", 20), ("📕 Expert", 30)]

            earned_badges = [badge for badge, threshold in badges if total_study_hours >= threshold]
            if earned_badges:
                st.write("🏅 **Badges Earned:** " + ", ".join(earned_badges))
            else:
                st.info("Keep studying to earn badges!")

elif st.session_state["page"] == "Pomodoro Timer":
    show_back_button()
    st.title("Pomodoro Timer ⏳")
    st.subheader("Stay Focused with Pomodoro Timer")
    # Initialize session state for Pomodoro tracking
    if "pomodoro_sessions" not in st.session_state:
        st.session_state.pomodoro_sessions = 0
    if "active_task" not in st.session_state:
        st.session_state.active_task = ""
    if "pomodoro_running" not in st.session_state:
        st.session_state.pomodoro_running = False

    # Task Input Box
    task_focus = st.text_input("Enter Task to Focus On", st.session_state.active_task)

    if task_focus:
        st.session_state.active_task = task_focus
        st.write(f"🎯 **Focusing on:** {st.session_state.active_task}")
    else:
        st.write("⚠️ Enter a task to focus on.")

    # User-defined Pomodoro cycle settings
    work_time = st.slider("Work Duration (minutes)", 5, 60, 25, key="work_duration")
    break_time = st.slider("Break Duration (minutes)", 1, 15, 5, key="break_duration")
    # Timer function using Streamlit Progress Bar
    def run_timer(seconds, label):
        progress_bar = st.progress(0)
        time_display = st.empty()
        for i in range(seconds):
            time.sleep(1)
            progress_bar.progress((i + 1) / seconds)
            time_display.write(f"{label} Time Remaining: {seconds - i} sec")
        time_display.empty()
        progress_bar.empty()

    col1, col2 = st.columns(2)

    # Start Pomodoro Timer Button
    with col1:
        if st.button("▶ Start Pomodoro Session", use_container_width=True):
            st.session_state.pomodoro_running = True
            st.write("🚀 **Work Session Started! Stay focused.**")
            run_timer(work_time * 60, "Work")

            if st.session_state.pomodoro_running:
                st.success("✅ Work Session Complete! Take a Break.")
                st.write("🛑 **Time for a break!**")
                run_timer(break_time * 60, "Break")

                # Session Completed
                st.session_state.pomodoro_sessions += 1
                st.success(f"🎉 Pomodoro Session {st.session_state.pomodoro_sessions} Completed!")

                # Motivational Break Suggestion
                break_suggestions = ["🌿 Stretch for 5 minutes.", "💧 Drink some water.", "🚶 Take a short walk.",
                 "🧘Do deep breathing exercises.", "📖 Read a few pages of a book."]
                st.info(f"💡 **Break Tip:** {random.choice(break_suggestions)}")

    # Finish Pomodoro Timer Button (ALWAYS VISIBLE)
    with col2:
        if st.button("❌ Finish Pomodoro Timer", use_container_width=True):
            st.session_state.pomodoro_running = False
            st.warning("⏹️ Pomodoro session ended early.")
            st.rerun()  # Restart the script to stop the session

elif st.session_state["page"] == "QR Code Generator":
    show_back_button()
    st.title("QR Code Generator 🔗")
    if not st.session_state["logged_in"]:
        st.warning("🔒 Please log in to access this feature.")
    else:
        if st.session_state["logged_in"]:
            st.subheader("QR Code Generator")
            # QR Code Type Selection
            qr_type = st.radio("Choose QR Code Type",
                               ["Text/URL", "Email", "Phone Number", "WiFi", "Event",
                                "SMS", "WhatsApp", "Google Maps"], horizontal=True)

            # Get input from user based on QR type
            qr_input = ""

            if qr_type == "Text/URL":
                qr_input = st.text_input("Enter Text or URL")

            elif qr_type == "Email":
                email = st.text_input("Enter Email Address")
                qr_input = f"mailto:{email}" if email else ""

            elif qr_type == "Phone Number":
                phone = st.text_input("Enter Phone Number")
                qr_input = f"tel:{phone}" if phone else ""

            elif qr_type == "WiFi":
                wifi_ssid = st.text_input("WiFi SSID (Network Name)")
                wifi_password = st.text_input("WiFi Password", type="password")
                encryption = st.selectbox("Encryption", ["WPA", "WEP", "None"])
                qr_input = f"WIFI:T:{encryption};S:{wifi_ssid};P:{wifi_password};;" if wifi_ssid else ""

            elif qr_type == "Event":
                event_title = st.text_input("Event Title")
                event_location = st.text_input("Event Location")
                event_date = st.date_input("Event Date")
                event_time = st.time_input("Event Time")
                qr_input = f"BEGIN:VEVENT\nSUMMARY:{event_title}\nLOCATION:{event_location}\nDTSTART:{event_date}T{event_time}\nEND:VEVENT" if event_title else ""

            elif qr_type == "SMS":
                sms_number = st.text_input("Phone Number")
                sms_message = st.text_area("Enter SMS Message")
                qr_input = f"sms:{sms_number}?body={sms_message}" if sms_number else ""

            elif qr_type == "WhatsApp":
                whatsapp_number = st.text_input("Enter WhatsApp Number (with country code)")
                qr_input = f"https://wa.me/{whatsapp_number}" if whatsapp_number else ""

            elif qr_type == "Google Maps":
                latitude = st.text_input("Latitude")
                longitude = st.text_input("Longitude")
                qr_input = f"https://www.google.com/maps?q={latitude},{longitude}" if latitude and longitude else ""

            # Generate QR Code Button
            if st.button("Generate QR Code"):
                def create_qr(data):
                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Low error correction
                        box_size=10,
                        border=4,
                    )
                    qr.add_data(data)
                    qr.make(fit=True)
                    return qr.make_image(fill_color="black", back_color="white")

                if qr_input:
                    qr_img = create_qr(qr_input)
                    img_byte_arr = io.BytesIO()
                    qr_img.save(img_byte_arr, format="PNG")
                    st.image(img_byte_arr.getvalue(), caption="Generated QR Code")
                    st.download_button("📥 Download QR Code",
                                       data=img_byte_arr.getvalue(),
                                       file_name="qr_code.png",
                                       mime="image/png")
                else:
                    st.error("⚠️ Please enter valid data.")

