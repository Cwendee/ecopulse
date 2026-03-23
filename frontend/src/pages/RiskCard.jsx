import { useNavigate } from "react-router-dom";
import {Risk} from "../constants/index";
import Button from "../components/ReUsables/Button";
import RightArrow from "../assets/svgIcons/right-arrow.svg?react";

const RiskCard = () => {

    const navigate = useNavigate();

    const level = "high";
    const riskLevel = Risk[level]
    const Icon = riskLevel.icon

    return ( 
        <section className="site-container">
            <div className="flex justify-center items-center">
                <div className={`${riskLevel.border} w-80 md:w-97 rounded-xl p-6 flex flex-col justify-center items-center gap-6 `} >
                    <div className={`icon-container ${riskLevel.bg} w-16 h-16 rounded-2xl p-3 flex justify-center items-center `}>
                     <Icon className="w-11 h-11" />
                    </div>
                    <p className="typo-xl" >{riskLevel.title} </p>
                    <p className="text-xl font medium text-center" >{riskLevel.content} </p>

                    <Button children={riskLevel.firstButton} rightSection={<RightArrow />} className="btn btn-primary btn-md text-xl " onClick={() => riskLevel.firstLink && navigate(riskLevel.firstLink)} />
                    <Button children={riskLevel.secondButton} rightSection={<RightArrow />} className="btn btn-accent btn-md text-xl " onClick={() => riskLevel.secondLink && navigate(riskLevel.secondLink)} />
                </div>
            </div>
        </section>
     );
}
 
export default RiskCard;