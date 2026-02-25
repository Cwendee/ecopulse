import Button from "../components/ReUsables/Button";
import LocationPointer from "../assets/svgIcons/location-pointer.svg?react";

import { useNavigate } from "react-router-dom";
import { pages } from "../constants/index.js";

const SignUp = () => {

    const navigate = useNavigate();

    return ( 
        <section className="signup site-container" >
            <div>
                <h1 className="text-[28px] md:text-[32px] lg:text-[56px] ">Flood Alert Notifications</h1>
                <p className="typo-3xl">Sign up with your email only and receive timely flood warnings.</p>

                <form className="flex flex-col justify-center items-start gap-4">

                    <label for="email" className="typo-2xl" >Email address</label>
                    <input type="email" id="email" placeholder="example@gmail.com" className="bg-white border border-[#296083] rounded-2xl py-1.75 px-5 w-full" />

                    <label for="location" className="typo-2xl" >Location</label>
                    <select name="country" id="location" className="w-[30%] bg-white border border-[#296083] rounded-2xl py-1.75 px-5">
                        <option value="" disabled>Select Country</option>
                    </select>

                    <input type="text" placeholder="Region" className="w-full bg-white border border-[#296083] rounded-2xl py-1.75 px-5" />
                    <Button children={"Use My Current Location"} rightSection={<LocationPointer />} className="btn btn-md btn-accent" />

                    <div className="flex flex-col justify-center items-start gap-1 mt-8 " >
                        <h2 className="typo-2xl" >Alert Preferences</h2>
                        <p className="typo-base" >Let us know what flood alert notifications you would like to receive. Select all which apply.</p>
                        <label className="text-xl flex justify-center items-center gap-3" > <input type="checkbox" name="severe-flood" className="w-6 h-6 rounded-sm border border-[#008B8B] accent-[#008B8B]" /> Severe flood warnings</label>

                        <label className="text-xl flex justify-center items-center gap-3" > <input type="checkbox" name="early-risk" id="" className="w-6 h-6 rounded-sm border border-[#008B8B] accent-[#008B8B]" /> Early risk alerts (rainfall + river levels)</label>

                        <label className="text-xl flex justify-center items-center gap-3"> <input type="checkbox" name="reminders" className="w-6 h-6 rounded-sm border border-[#008B8B] accent-[#008B8B]" /> Preparedness reminders</label>
                    </div>

                    <div className="flex flex-col justify-center items-start gap-1 mt-8 " >
                        <h2 className="typo-2xl" >Delivery</h2>
                        <p className="typo-base" >How would you like to receive notifications? Select all which apply.</p>
                        <label className="text-xl flex justify-center items-center gap-3" > <input type="checkbox" name="email" className="w-6 h-6 rounded-sm border-none accent-[#008B8B]" /> Email alerts only</label>

                        <label className="text-xl flex justify-center items-center gap-3" > <input type="checkbox" name="app" className="w-6 h-6 rounded-sm border border-[#008B8B] accent-[#008B8B]" /> In-app alerts</label>

                        <label className="text-xl flex justify-center items-center gap-3"> <input type="checkbox" name="browser" className="w-6 h-6 rounded-sm border border-[#008B8B] accent-[#008B8B]" /> Browser notifications</label>
                    </div>

                    <Button children={"Submit"} className="btn btn-primary btn-md my-5" onClick={() => pages.chat && navigate(pages.chat)}/>

                </form>
            </div>

        </section>
     );
}
 
export default SignUp;