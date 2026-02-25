import Chat from "../assets/svgIcons/chatbot.svg?react";
import Emoji from "../assets/svgIcons/emoji.svg?react";
import Attach from "../assets/svgIcons/attach.svg?react";
import Menu from "../assets/svgIcons/menu-dots.svg?react";

const ChatBot = () => {
    return ( 
        <section className="site-container">
            <div className="flex flex-col gap-6.5 md:gap-16.5 ">
                <div className="flex items-center gap-3 md:gap-10 bg-[#03A199] px-5 md:px-10 py-5 rounded-[30px] " >
                    <Chat className="w-20 h-20 md:w-25 md:h-25" />
                    <p className="text-[20px] md:text-[40px] " >Hey there! Have questions? I’m here to help</p>
                </div>

                <div className="chat-container flex flex-col gap-7.5 md:gap-12.5" >
                    <div className="user-question border-5 border-[#95E06C] rounded-3xl md:rounded-[30px] min-h-16.25 md:min-h-26.25 ">

                    </div>
                    <div className="chatbox-response border-5 border-[#95E06C] bg-[#92C0DD] rounded-3xl md:rounded-[30px] min-h-16.25 md:min-h-26.25 "></div>
                </div>

                <div className="relative" >
                    <textarea name="user-question" id="" placeholder="Ask anything..." className="border-7 border-[#296083] w-full rounded-[20px] h-30 md:h-42.5 px-5 md:px-7 py-3 md:py-5 typo-2xl " >
                    </textarea>

                    <div className="flex absolute bottom-4 px-7 ">
                        <Emoji className="w-7 md:w-9 h-7 md:h-9"/>
                        <Attach className="w-7 md:w-9 h-7 md:h-9"/>
                        <Menu className="w-7 md:w-9 h-7 md:h-9"/>
                    </div>
                    
                </div>
                    
            </div>
        </section>
     );
}
 
export default ChatBot;