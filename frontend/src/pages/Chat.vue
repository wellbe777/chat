<template>
    <div class="main-container">
    <div class="chat-container">
    <div v-if="creationVisible" class="modal">
    <div class="chatroom-modal">
        <div class="alert alert-danger" role="alert" v-if="creationError">{{ creationError }}</div>
        <p class="main_text">{{$t('enter_new_chatroom_name')}}</p>
        <div class="input-group mb-3">
             <input type="text" class="text-input" style="" placeholder="" v-model="chatroomName">
        </div>
        <div class="d-flex justify-content-center" style="gap: 10px;margin-top: 20px;">
            <button type="submit" class="btn btn-primary" v-on:click="createChatRoom">{{$t('ok')}}</button>
            <button type="submit" class="btn btn-primary" v-on:click="this.creationVisible = false">{{$t('cancel')}}</button>
        </div>
    </div>
    </div>
    <div class="box left" id="chatList">
        <button type="submit" class="btn btn-primary center" v-on:click="this.creationVisible = true"> {{$t('create_chat_room')}} </button>
        <div class="channel-list" v-if="Object.keys(channel_list).length">
            <div v-for="channel in channel_list" :key="channel.chat_name" class="item-container">
                <button style="box-shadow: none" :class="['button', { selected: selectedButton === channel.chat_name }]" v-on:click="buttonClicked(channel.chat_name)">
                    <div class="chatname-text">{{channel.chat_name}}</div>
                    <div class="author-text">{{$t('author', {author: channel.author})}}</div>
                </button>
            </div>
        </div>
    </div>
    <div class="box center">
    <div class="container">
        <p class="main_text" style="margin: 0 auto 15px auto">{{$t('chat')}}</p>
        <transition>
            <button v-if="isAuthor" type="submit" v-on:click="deleteChatRoom" class="btn btn-primary top-right">
                    <i class="bi bi-trash3-fill" style="color:var(--delete-color)"></i>
            </button>
        </transition>
    </div>
      <div class="chatbox-body" ref="chatboxBody">
            <transition>
                <div v-if="loading" class="loading-screen">
                    <div class="spinner-border" style="animation: spinner-border 1s linear infinite;"></div>
                    <p>{{ $t(loading_message) }}</p>
                </div>
            </transition>
            <div v-if="messages_list[selectedButton]" v-for="v in messages_list[selectedButton]">
                <span class="chat-message" style="color: var(--gray-color)">{{ v.username + ": " }}</span>
                <span class="chat-message">{{ v.message }}</span>
                <br/>
            </div>
      </div>
      <div class="d-flex">
            <button @click="toggleEmojiPicker" class="btn btn-primary" style="margin-bottom: 2px;">😀</button>
            <input class="text-input" type="text" @keyup.enter="sendMessage" style="border-radius: 8px 0px 0px 8px;" v-model="message" :placeholder="$t('type_message')">
            <div class="separator"></div>
            <button type="submit" v-on:click="sendMessage" class="btn btn-primary send"> 
                <i class="bi bi-send-fill"></i> 
            </button>
        </div>
        <div v-if="showEmojiPicker" class="emoji-picker-popup">
            <EmojiPicker native="true" disable-skin-tones="true" theme="dark" @select="onSelectEmoji" />
        </div>
    </div>
</div>
</div>
</template>
<script>
import { useCookies } from "vue3-cookies";
import axios from 'axios'
import EmojiPicker from 'vue3-emoji-picker'
import 'vue3-emoji-picker/css'
import Navigation from '../components/Navigation.vue'
export default {
    name: "Chat",
    components: {
        EmojiPicker,
        Navigation
    },
    data() {
        return {
            message: '',
            websocket: null,
            selectedButton: null,
            loading_message: 'connecting',
            loading: true,
            channel_list: [],
            messages_list: [],
            creationVisible: false,
            chatroomName: '',
            creationError: '',
            isAuthor: false,
            showEmojiPicker: false
        }
    },
    mounted() {
        this.CreateWS()
    },
    methods: {
        scrollToBottom() {
            setTimeout(() => {
                const messagesContainer = this.$refs.chatboxBody
                if (messagesContainer) messagesContainer.scrollTop = messagesContainer.scrollHeight
            }, 100)
        },
        onSelectEmoji(emoji) {
            this.message = this.message + emoji.i
        },
        toggleEmojiPicker() {
            this.showEmojiPicker = !this.showEmojiPicker;
        },
        deleteChatRoom() {
            if (!this.selectedButton || this.selectedButton == "") return;
            const { cookies } = useCookies()
            const token = cookies.get('jwt')
            this.websocket.send(JSON.stringify({
                    type: 3,
                    jwt: token,
                    chat_name: this.selectedButton
            }))
        },
        createChatRoom() {
            if (this.chatroomName == "" || this.chatroomName.length <= 0) return;
            const { cookies } = useCookies()
            const token = cookies.get('jwt')
            this.websocket.send(JSON.stringify({
                    type: 2,
                    jwt: token,
                    chat_name: this.chatroomName
            }))
            // this.creationVisible = false
            // this.chatroomName = ""
            if (this.loading && this.websocket.readyState === WebSocket.OPEN) {
                this.loading = false
            }
        },
        addToChatRoom(channel){
            const { cookies } = useCookies()
            const token = cookies.get('jwt')
            this.websocket.send(JSON.stringify({
                    type: 4,
                    jwt: token,
                    chat_name: channel
            }))
        },
        buttonClicked(channel) {
            if (this.selectedButton == channel) return;
            this.messages_list = []
            this.addToChatRoom(channel)
            const { cookies } = useCookies()
            axios.get("http://localhost:8000/chat/api", {params: {request_type: 2, channel_name: channel}})
            .then((e) => {
                const data = e.data
                for(let i=0; i < data.length; ++i) {
                    const msg = data[i]
                    if (!this.messages_list[msg.chat_name]) this.messages_list[msg.chat_name] = [];
                    const tbl = this.messages_list[msg.chat_name]
                    tbl.push({username: msg.username, message: msg.message})
                }
            })
            .catch((e) => {
                const resp = e.response
                if (resp.status == 403) {
                    cookies.remove('jwt')
                    cookies.remove('signature')
                    this.$router.push("/login")
                }
            })
            if (this.loading && this.websocket.readyState === WebSocket.OPEN) {
                this.loading = false
            }
            this.selectedButton = channel
            this.isAuthor = this.channel_list[channel].author === atob(cookies.get('signature'))
            this.scrollToBottom()
        },
        AddChatList(switch_channel, channel) {
            const { cookies } = useCookies()
            axios.get("http://localhost:8000/chat/api", {params: {request_type: 1}})
                .then((e) => {
                    setTimeout(() => {
                        if (e.data.length <= 0 && !this.loading) {
                            this.loading = true
                            this.loading_message = 'create_channel_first'
                            this.channel_list = []
                            return
                        }
                    }, 1000)
                    if (e.data.length <= 0) {
                        this.loading = true
                        this.loading_message = 'create_channel_first'
                        this.channel_list = []
                        return
                    }
                    this.channel_list = e.data.reduce((tbl, obj) => {
                        tbl[obj.chat_name] = obj;
                        return tbl
                    }, {});
                    if (switch_channel) {
                        const newChat = channel && channel || e.data[0].chat_name
                        this.buttonClicked(newChat)
                        this.isAuthor = this.channel_list[newChat].author === atob(cookies.get('signature'))
                    }
                })
                .catch((e) => {console.log(e)})
        },
        CreateWS() {
            this.websocket = new WebSocket('ws://localhost:8000/chat');
            const { cookies } = useCookies()
            this.websocket.onopen = () => {
                const token = cookies.get('jwt')
                this.websocket.send(JSON.stringify({
                    type: 1,
                    jwt: token
                }));
                setTimeout(() => {
                this.loading = false;
                }, 1000);
                this.AddChatList(true)
            };

            this.websocket.onmessage = (event) => {
                try {
                    const json = JSON.parse(event.data)
                    if (json.data_type === 'bulk_messages') {
                        if (json.data.length <= 0) {
                            this.loading = true
                            this.loading_message = 'create_channel_first'
                            this.messages_list = []
                            return
                        }
                        const data = json.data
                        for(let i=0; i < data.length; ++i) {
                            const msg = data[i]
                            if (!this.messages_list[msg.chat_name]) this.messages_list[msg.chat_name] = [];
                            const tbl = this.messages_list[msg.chat_name]
                            tbl.push({username: msg.username, message: msg.message})
                        }
                        this.scrollToBottom()
                    } else if (json.data_type === 'message') {
                        if (!this.messages_list[json.chat_name]) this.messages_list[json.chat_name] = [];
                        const tbl = this.messages_list[json.chat_name]
                        tbl.push({username: json.username, message: json.message})
                        if (json.username === atob(cookies.get('signature'))) this.scrollToBottom(); 
                    } else if (json.data_type === "chat_creation") {
                        if (json.msg === 'success') {
                            this.AddChatList(true, this.chatroomName)
                            this.creationVisible = false
                            this.chatroomName = ""
                        } else {
                            this.creationError = json.msg
                        }
                    } 
                    else if (json.data_type === 'chat_deletion') {
                        if (json.msg === 'success') {
                            this.messages_list[json.chat_name] = []
                            this.AddChatList(true)
                        }
                    }
                } catch (e) {
                    console.log('Error:', e.message);
                }
            };
            this.websocket.onclose = (event) => {
                const { cookies } = useCookies()
                if (event.code == 4001) {
                    cookies.remove('jwt')
                    cookies.remove('signature')
                    this.$router.push("/login")
                    return
                }
                this.loading = true
                this.showEmojiPicker = false
                this.loading_message = 'reconnecting'
                this.messages_list = []
                this.CreateWS()
            };
        },
        SendWSMessage(token, message) {
            this.websocket.send(JSON.stringify({
                    type: 5,
                    jwt: token,
                    message: message
            }))
        },
        async sendMessage() {
            if (!this.message || this.message == "" || this.message.trim() == '') return;
            const { cookies } = useCookies()
            const token = cookies.get('jwt')
            if (!token) {
                cookies.remove('signature')
                this.$router.push("/login")
                return
            }
            this.SendWSMessage(token, this.message)
            this.message = ""
            this.showEmojiPicker = false
        },
    }
};
</script>
<style scoped>
.main-container {
    display: flex;
    flex-direction: column;
    overflow-y: hidden;
}
.chat-container {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}

.box {
    position: relative;
    border-radius: 8px;
    background-color: var(--primary-color-95);
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
    max-width: 500px;
    padding: 20px;
    transition: width 0.5s ease, height 0.5s ease;
    box-sizing: border-box;
    flex: 1;
    min-width: 0;
}

.box.center {
    left: auto;
    top: auto;
}

.box.left {
    max-width: 300px;
    left: auto;
    top: auto;
    padding: 10px;
    margin: 0 10px;
}

.channel-list {
    position: relative;
    width: 100%;
    height: 400px;
    overflow-x: hidden;
    overflow-y: auto;
}
@media (min-width: 600px) and (min-height: 650px) {
    .chat-container {
        height: 85vh;
    }
}
@media (max-width: 600px), (max-height: 650px) {
    .chat-container {
        flex-direction: column;
        padding: 10px;
    }
    .box.center {
        width: 90%;
        padding: 15px;
        margin-top: 30px;
    }
    .box.left {
        width: 90%;
        max-width: 500px;
        left: 0px;
        top: 10px;
        padding: 15px;
    }
}

.button {
    display: block;
    width: 100%;
    border: none;
    background-color: #04AA6D;
    color: white;
    margin: 3px;
    padding: 5px 10px;
    font-size: 16px;
    cursor: pointer;
    text-align: left;
}
.chatname-text {
    font-size: 16px;
    font-weight: bold;
}
.modal {
    position: fixed;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
}

.chatroom-modal {
    background-color: rgba(22, 22, 22, 1);
    margin: auto;
    padding: 20px;
    width: 100%;
    max-width: 400px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    text-align: center;
}

.input-group.mb-3 {
    color: #ffff !important;
    background-color: transparent !important;
}

.author-text {
    font-size: 10px;
    color: #666;
}

.selected {
    background-color: #4CAF50;
    color: white;
}

.chatbox-body {
    position: relative;
    padding: 5px;
    height: 400px;
    overflow-y: auto;
    background-color: var(--box-color);
    color: var(--text-color);
    white-space: normal;
    overflow-wrap: break-word;
}

.chat-message {
    text-align: left;
    color: var(--text-color);
}

.main_text {
    font-size: 1.5rem;
    color: #CCC;
    text-align: center;
}

.emoji-picker-popup {
  position: absolute;
  bottom: 60px;
  z-index: 1001;
}

.btn.btn-primary.center {
  position: relative;
  left: 50%;
  transform: translate(-50%, -50%);
  margin-top: 21px;
  margin-bottom: -8px;
}
.btn.btn-primary.top-right {
  position: absolute;
  right: 20px;
  margin-bottom: 15px;
  font-size: 16px;
}

.btn.btn-primary.send {
  border-radius: 0px var(--bs-btn-border-radius) var(--bs-btn-border-radius) 0px;
  margin-top: 8px;
  transform: none;
  transition: none;
  box-shadow: none;
}

.text-input {
    box-sizing: border-box;
    display: block;
    width: 100%;
    margin-left: 3px;
    margin-top: 8px;
    padding: 10px 15px;
    border: 3px solid transparent;
    color: currentColor;
    background-color: var(--box-color);
    border-radius: 8px;
    outline: none;
    font-size: 15px;
    color: var(--text-color);
}

.separator {
    margin-top: 8px;
    width: 2px;
    background-color: var(--separator-color);
}

.container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
    box-sizing: border-box;
}

.loading-screen {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--loading-screen-color);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.spinner-border {
    width: 25px;
    height: 25px;
    margin-bottom: 10px;
    margin-right: 8px;
}

.v-enter-active, .v-leave-active {
  transition: opacity 0.3s ease;
}

.v-enter-from, .v-leave-to {
  opacity: 0;
}

</style>