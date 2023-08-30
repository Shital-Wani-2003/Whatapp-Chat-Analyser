import streamlit as st
import preprocesser
import helper
import matplotlib.pyplot as plt


st.sidebar.title("whatsapp chat Analyzer")


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # to convart into string
    data = bytes_data.decode("utf-8")
    #st.text(data) #data of file looks on screen
    df=preprocesser.preprocesser(data)

    st.dataframe(df)

    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user=st.sidebar.selectbox("show analysis wrt", user_list)

    if st.sidebar.button("Show analysis"):
        col1, col2 ,col3 ,col4= st.columns(4)
        num_messages,words,num_media_msg, links=helper.fetch_stats(selected_user,df)

        with col1:
            st.header("Total message")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_msg)

        with col4:
            st.header("links Shared")
            st.title(links)

        #Finding The busiest user in group
        if selected_user == 'Overall':
            st.title("Most Busy users")
            x,new_df=helper.most_busy_users(df)
            fig, ax= plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        #wordcloud
        st.title("worldcloud")
        df_wc =helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        most_common_df = helper.most_common_words(selected_user, df)
        fig,ax =plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most common words')
        st.pyplot(fig)

        # emoji_df = helper.emoji_helper(selected_user, df)
        # st.dataframe()














