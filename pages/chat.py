import streamlit as st
from streamlit_chat import message
import openai
import os
import Source.response as Response
import Source.promptInitialization as PromptInisilization
#import Source.mcta as MCTS
import json
import Source.treegraph as treeBuild
#import Source.treegraphCriteria as treeBuildCriteria
from langchain.memory import ConversationBufferMemory
from streamlit_cookies_controller import CookieController
from streamlit_autorefresh import st_autorefresh
cookie_controller = CookieController()
from time import sleep
from datetime import datetime, UTC, timedelta
from navigation import make_sidebar
make_sidebar()
memory = ConversationBufferMemory(human_prefix="human", ai_prefix="AI",memory_key="history", return_messages=True)


USER_NAME = "user"
ASSISTANT_NAME = "assistant"
State_component = "State"
end_greeting = ['Thanks','thanks','Thank You','thank you','Thanks for your information','thanks for your instruction', 'thanks for your suggestions']

message_history = []

patient_messages = []
therapist_messages = []
therapist_messages_last_utterace = ""
patient_messages_last_utterace = ""
subset_list =[]
formatted_data = []

if "depression_level" not in st.session_state:
    st.session_state.depression_level = None

if "anxiety_level" not in st.session_state:
    st.session_state.anxiety_level = None
    
def archive_messages(log_conversation_from_session):
    # Iterate through messages and separate them based on the 'Name' key
    """
    for message in log_conversation_from_session:
        message_history.append((message['Name'],':', message['msg'],' \n'))

    print("The Message")
    print(message_history)"""
    
    for message in log_conversation_from_session:
        if message['name'] == 'user':
            patient_messages.append(message['msg'])
        elif message['name'] == 'assistant':
            therapist_messages.append(message['msg'])
    
    for i in range(len(patient_messages)):
        message_history.append("Patient :" + patient_messages[i] + '\n')
        message_history.append("Therapist :" + therapist_messages[i] + '\n')

## Depression Enter Form Code
if cookie_controller.get('Depression') is None and cookie_controller.get('Anxiety') is None:
    st.title("Enter Your PHQ-9 Information")

    CHOICES = {0: "Not at all", 1: "Several days", 2: "More than half the days", 3:"Nearly every day"}

    def format_func(option):
        return CHOICES[option]


    phq_1 = st.selectbox("1 Little interest or pleasure in doing things", options=list(CHOICES.keys()), format_func=format_func)
    phq_2 = st.selectbox("2 Feeling down, depressed, or hopeless", options=list(CHOICES.keys()), format_func=format_func)
    phq_3 = st.selectbox("3 Trouble falling or staying asleep, or sleeping too much", options=list(CHOICES.keys()), format_func=format_func)

    phq_4 = st.selectbox("4 Feeling tired or having little energy", options=list(CHOICES.keys()), format_func=format_func)
    phq_5 = st.selectbox("5 Poor appetite or overeating", options=list(CHOICES.keys()), format_func=format_func)
    phq_6 = st.selectbox("6 Feeling bad about yourself   or that you are a failure or have let yourself or your family down", options=list(CHOICES.keys()), format_func=format_func)

    phq_7 = st.selectbox("7 Trouble concentrating on things, such as reading the newspaper or watching television", options=list(CHOICES.keys()), format_func=format_func)
    phq_8 = st.selectbox("8 Moving or speaking so slowly that other people could have noticed. Or the opposite being so figety or restless that you have been moving around a lot more than usual", options=list(CHOICES.keys()), format_func=format_func)
    phq_9 = st.selectbox("9 Thoughts that you would be better off dead, or of hurting yourself", options=list(CHOICES.keys()), format_func=format_func)

    if st.button("Submit", type="primary"):
        total_score = phq_1 + phq_2 + phq_3 + phq_4 + phq_5 + phq_6 + phq_7 + phq_8 + phq_9
        Depression_label = None
        if total_score >0 and total_score<4:
            Depression_label = "No depression"
        elif total_score>4 and total_score<=9:
            Depression_label = "Mild depression"
        elif total_score>9 and total_score<=14:
            Depression_label = "Moderate depression"
        elif total_score>14 and total_score<=19:
            Depression_label = "Moderately severe depression"
        elif total_score>19:
            Depression_label = "Severe depression"
        
        st.session_state.depression_level = Depression_label
        
        # if Depression_label != "No depression":
        st.success("Your PHQ-9 Information Successfully Inserted")
        # expires_at = datetime.now(UTC) + timedelta(minutes=2)
        cookie_controller.set('Depression','Depression_label')
        st_autorefresh(interval=1000, limit=100, key="fizzbuzzcounter")
        #st.experimental_rerun()
        sleep(3)

# Anxiety Form Code
if cookie_controller.get('Depression')is not None and cookie_controller.get('Anxiety') is None:
 
   st.title("Enter Your GAD-7 Information")

   CHOICES = {0: "Not at all", 1: "Several days", 2: "More than half the days", 3:"Nearly every day"}

   def format_func(option):
     return CHOICES[option]


   gad_1 = st.selectbox("1 Feeling nervous, anxious or on edge?", options=list(CHOICES.keys()), format_func=format_func)
   gad_2 = st.selectbox("2 Not being able to stop or control worrying?", options=list(CHOICES.keys()), format_func=format_func)
   gad_3 = st.selectbox("3 Worrying too much about different things?", options=list(CHOICES.keys()), format_func=format_func)

   gad_4 = st.selectbox("4 Trouble relaxing?", options=list(CHOICES.keys()), format_func=format_func)
   gad_5 = st.selectbox("5 Being so restless that it is hard to sit still?", options=list(CHOICES.keys()), format_func=format_func)
   gad_6 = st.selectbox("6 Becoming easily annoyed or irritable?", options=list(CHOICES.keys()), format_func=format_func)

   gad_7 = st.selectbox("7 Feeling afraid as if something awful might happen?", options=list(CHOICES.keys()), format_func=format_func)

   if st.button("Enter", type="primary"):
        total_score = gad_1 + gad_2 + gad_3 + gad_4 + gad_5 + gad_6 + gad_7 
        Anxiety_label = None
        if total_score >0 and total_score<4:
         Anxiety_label = "No anxiety"
        elif total_score>4 and total_score<=9:
         Anxiety_label_label = "Mild anxiety"
        elif total_score>9 and total_score<=14:
         Anxiety_label_label = "Moderate anxiety"
        elif total_score>14:
         Anxiety_label = "Severe anxiety"
        
        st.session_state.anxiety_level = Anxiety_label
            
        # if Anxiety_label != "No anxiety":
        st.success("Your GAD-7 Information Successfully Inserted")
        # expires_at = datetime.now(UTC) + timedelta(minutes=2)
        cookie_controller.set('Anxiety','{Anxiety_label}')
        st_autorefresh(interval=1000, limit=100, key="fizzbuzzcounter")
        sleep(2)


# cookie_controller.remove("Depression")
# cookie_controller.remove("Anxiety")

# Chat Form 
if cookie_controller.get('Depression') is not None and cookie_controller.get('Anxiety') is not None:
    print(cookie_controller.get('Depression'))
    print(cookie_controller.get('Anxiety'))
    st.title("Well-Being Support For Student")
    if "chat_log" not in st.session_state:
        st.session_state.chat_log = []
        st.session_state.state_log = []

    utterance_list = []
    user_msg = st.chat_input("Enter Your Thought")

    if 'count' not in st.session_state: 
        st.session_state.count = 0

    if st.chat_input:
        st.session_state.count += 1
    
    if 'FlagState' not  in st.session_state:
        st.session_state.FlagState = None
    
    # if 'chat_history' not in st.session_state:
    #     st.session_state.chat_history = None
    
    if "action" not in st.session_state:
        st.session_state.action = None
    
    if "state_value" not in st.session_state:
        st.session_state.state_value = None
   
    if "selfdis_value" not in st.session_state:
        st.session_state.selfdis_value = 1
    
    print('Count = ' + str(st.session_state.count))

    if user_msg:
        for chat in st.session_state.chat_log:
            with st.chat_message(chat["name"]):
                st.write(chat["msg"])

        with st.chat_message(USER_NAME):
            st.write(user_msg)
        
        # if 'action' not in st.session_state:
        #     st.session_state.action = None

        # promptInitilize and StateDefine
        # stateSelectionPrompt = PromptInisilization.stateDefine(history, user_msg)
       
        if st.session_state.count >= 1:
            # if st.session_state.FlagState != True:  
            #     dialogueStatePrompt = PromptInisilization.dialogueStatePrompt(st.session_state.chat_history, user_msg)
            #     dialogueState = Response.dialogueStateDetection(dialogueStatePrompt)
            #     state_information = json.loads(dialogueState)
            #     state_value = int(state_information["predictions"]["state"])
            #     if state_value == 1:
            #         st.session_state.state_value = True
            #     print("State value:", state_value)
            
            # archive_messages(st.session_state.chat_log)
            # if st.session_state.FlagState != True:
            #     if (state_value == 0 and st.session_state.count < 7) or st.session_state.count < 7:
            #         # problem understand
            #         promptType = PromptInisilization.self_explorer(message_history,user_msg)
                    
            #         # Save in Memory for Management
            #         if st.session_state.chat_history is None:
            #            st.session_state.chat_history = []
            #         else:
            #            for message in st.session_state.chat_history:
            #               memory.save_context({'input':message['human']},{'output':message['AI']})
                    
            #         response = Response.response_Generation_from_GPT4_test(promptType,user_msg,memory)

            #         print("Final Response: ",response)

            #         # Save in Session
            #         message = {'human':user_msg,'AI':response}
            #         st.session_state.chat_history.append(message)

            #         if (st.session_state.state_value == True and st.session_state.count > 5) or st.session_state.count == 6:
            #         # if st.session_state.count == 6:
            #             st.session_state.FlagState = True
            
            # elif st.session_state.FlagState == True:
                
            # Determine The Reward
            Subset_prompt  = PromptInisilization.determine_reward_final(message_history,user_msg,st.session_state.action)
            actual_reward = Response.SubsetSelection(Subset_prompt)
            print("Before Extract Reawrd: ",actual_reward)
            reward_data = json.loads(actual_reward)
            print("Reward After Json Data", reward_data)
            
            # Determine The Reward with Criteria OpenAI
            # Subset_prompt  = PromptInisilization.subset_detection_with_weight(message_history,user_msg,st.session_state.action)
            # actual_reward = Response.SubsetSelection(Subset_prompt)
            # print("Before Extract Reawrd: ",actual_reward)
            # reward_data = json.loads(actual_reward)
            # print("Reward After Json Data", reward_data)

            # Determine The Reward with Criteria Antropic
            # Subset_prompt  = PromptInisilization.subset_detection_with_weight(message_history,user_msg,st.session_state.action)
            # actual_reward = Response.SubsetSelection_Anthropic_test(Subset_prompt)
            # print("Before Extract Reawrd: ",actual_reward)
            # reward_data = json.loads(actual_reward)
            # print("Reward After Json Data", reward_data)
        
        
            # Data Extraction
            best_action = treeBuild.dataImport(reward_data)

            st.session_state.action = best_action
            
            history = archive_messages(st.session_state.chat_log)
            print(history)
            
            # MCTS Code Implimentation
            # mcts_prompt = PromptInisilization.MCTS_prompt(message_history,user_msg)
            # subset = MCTS.testMCTS(mcts_prompt)
            # print("Test Subset from MCTS", subset)
            # subset = "problem_understand"

            
            # promptType = PromptInisilization.EnglishConversationPromptForGPT4oV8_testing(message_history,best_action,user_msg)
            # promptType = PromptInisilization.EnglishConversationPromptFor_Student_V11(message_history,best_action,user_msg)
            promptType = PromptInisilization.dbt_supportV3(message_history,best_action,user_msg,st.session_state.depression_level,st.session_state.anxiety_level)
            # promptType = PromptInisilization.JapaneseConversationPromptFor_Student_V12(message_history,best_action,user_msg)
            # promptType = PromptInisilization.EnglishConversationPromptForGPT4oV7_japansese(message_history,best_action,user_msg)
        
            # promptType = PromptInisilization.JapaneseConversationPromptForGPT4o(message_history,subset,patient_messages)
        
            # Save in Memory for Management
            
            if 'chat_history' not in st.session_state:
                st.session_state.chat_history = []
            else:
                for message in st.session_state.chat_history:
                    memory.save_context({'input':message['human']},{'output':message['AI']})

            # Response Generation
            #response = Response.response_generation_from_antropic(promptType,user_msg,memory)
            response = Response.response_Generation_from_GPT4_test(promptType,user_msg,memory)
            
            if st.session_state.selfdis_value == 1:
                response =  response +" "+ "Finally, Keep in mind this is the problem understanding phase, I want to understand you to support you best."  
                # response =  response +'  '+ "最後に、これは問題を理解するための段階であることを忘れないでください。あなたをできるだけよく支えるために、私はあなたのことを理解したいと思っています。"
                st.session_state.selfdis_value += 2
            
            print("Final Response: ",response)
            
            # Save in Session
            message = {'human':user_msg,'AI':response}
            st.session_state.chat_history.append(message)

        with st.chat_message(ASSISTANT_NAME):
            assistant_msg = ""
            assistant_response_area = st.empty()
            
            # for chunk in response:
            tmp_assistant_msg = response
            assistant_msg += tmp_assistant_msg
            assistant_response_area.write(assistant_msg)

        # st.session_state.state_log.append({"name": State_component, "msg": best_action})
        # print("State Log Print for the system: ", st.session_state.state_log )
        st.session_state.chat_log.append({"name": USER_NAME, "msg": user_msg})
        st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": assistant_msg})

