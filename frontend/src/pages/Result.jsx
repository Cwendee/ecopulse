import { useNavigate } from "react-router-dom";
import { pages } from "../constants/index.js";
import Success from "../assets/svgIcons/success.svg?react";
import Error from "../assets/svgIcons/error.svg?react";
import Button from "../components/ReUsables/Button.jsx";

const Result = () => {
    const navigate = useNavigate();

    let result = true;

    return ( 
        <div className="result-popup site-container flex justify-center bg-black/40 h-screen fixed">
            {
                result ? 
                (<div className="w-71 h-61 md:w-102 md:h-85.5 rounded-xl ">
                    <div className="upper h-[50%] bg-[#32CD32] flex flex-col justify-center items-center gap-1 md:gap-4.5 rounded-t-xl">
                        <Success />
                        <p className="text-white text-[24px] md:text-3xl font-medium" >Success!</p>
                    </div>
                    <div className="lower h-[50%] bg-[#F8F8FF] flex flex-col justify-center items-center gap-4.5 rounded-b-xl">
                        <p className="text-base md:text-xl text-center font-medium" >You’re ready to receive flood alerts.</p>
                        <Button children={"Continue to Home"} className="btn btn-primary btn-md" onClick={() => pages.home && navigate(pages.home)} />
                    </div>
                </div>)
                :
                (<div className="w-67 h-65 rounded-xl ">
                    <div className="upper h-[50%] bg-[#E34234] flex flex-col justify-center items-center gap-1 md:gap-4.5 rounded-t-xl">
                        <Error />
                        <p className="text-white text-xl font-medium" >Error!</p>
                    </div>
                    <div className="lower h-[50%] bg-[#F8F8FF] flex flex-col justify-center items-center gap-4.5 rounded-b-xl">
                        <p className="text-sm text-center font-medium" >Oops! Something went wrong. Make sure to fill the required fields.</p>
                        <Button children={"Try Again"} className="btn btn-primary btn-md" onClick={() => pages.home && navigate(pages.home)} />
                    </div>
                </div>)
            }
        </div>
        

     );
}
 
export default Result;