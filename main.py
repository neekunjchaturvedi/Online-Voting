import streamlit as st
from auth import register_user, authenticate_user
from voting import get_all_candidates, cast_vote, get_user_vote, get_vote_results

def main():
    st.title("Online Voting System")
    
    # Session state initialization
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = None
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    
    # Sidebar for authentication
    sidebar_auth()
    
    # Main content
    if st.session_state['logged_in']:
        show_voting_interface()
    else:
        st.info("Please login or register to access the voting system.")
        st.write("This online voting system allows you to:")
        st.write("- Cast your vote for your preferred candidate")
        st.write("- View your current vote")
        st.write("- See real-time voting results")

def sidebar_auth():
    st.sidebar.title("Authentication")
    
    if st.session_state['logged_in']:
        st.sidebar.success(f"Logged in as {st.session_state['username']}")
        if st.sidebar.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['user_id'] = None
            st.session_state['username'] = None
            st.experimental_rerun()
    else:
        auth_option = st.sidebar.radio("Choose option", ["Login", "Register"])
        
        if auth_option == "Login":
            with st.sidebar.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit_button = st.form_submit_button("Login")
                
                if submit_button:
                    if username and password:
                        success, user_id = authenticate_user(username, password)
                        if success:
                            st.session_state['logged_in'] = True
                            st.session_state['user_id'] = user_id
                            st.session_state['username'] = username
                            st.experimental_rerun()
                        else:
                            st.error("Invalid username or password")
                    else:
                        st.error("Please enter both username and password")
        
        else:  # Register
            with st.sidebar.form("register_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                submit_button = st.form_submit_button("Register")
                
                if submit_button:
                    if not username or not password:
                        st.error("Please enter both username and password")
                    elif password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        success, message = register_user(username, password)
                        if success:
                            st.success(message)
                            st.info("You can now login with your credentials")
                        else:
                            st.error(message)

def show_voting_interface():
    tab1, tab2, tab3 = st.tabs(["Vote", "My Vote", "Results"])
    
    with tab1:
        st.header("Cast Your Vote")
        candidates = get_all_candidates()
        
        with st.form("voting_form"):
            candidate_names = [candidate.name for candidate in candidates]
            selected_candidate = st.radio("Choose a candidate:", candidate_names)
            submit_button = st.form_submit_button("Submit Vote")
            
            if submit_button:
                # Get candidate ID from selected name
                candidate_id = next((c.id for c in candidates if c.name == selected_candidate), None)
                
                if candidate_id:
                    success, message = cast_vote(st.session_state['user_id'], candidate_id)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
    
    with tab2:
        st.header("My Vote")
        user_vote = get_user_vote(st.session_state['user_id'])
        
        if user_vote:
            st.write(f"You have voted for: **{user_vote.name}**")
            st.write(f"Description: {user_vote.description}")
        else:
            st.info("You haven't cast a vote yet. Go to the 'Vote' tab to vote.")
    
    with tab3:
        st.header("Voting Results")
        results = get_vote_results()
        
        # Create a bar chart of results
        if results:
            st.subheader("Current Vote Distribution")
            
            # Create data for the chart
            candidate_names = [result['name'] for result in results]
            vote_counts = [result['votes'] for result in results]
            
            # Display bar chart
            st.bar_chart(dict(zip(candidate_names, vote_counts)))
            
            # Display table of results
            st.subheader("Leaderboard")
            for i, result in enumerate(results):
                st.write(f"{i+1}. **{result['name']}**: {result['votes']} votes")
        else:
            st.info("No votes have been cast yet.")

if __name__ == "__main__":
    main()