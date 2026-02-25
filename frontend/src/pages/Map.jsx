<<<<<<< HEAD
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import Button from "../components/ReUsables/Button"
import RiskCard from "../pages/RiskCard"

const Map = () => {
    return ( 
        <section className="map site-container" >
            <div>
                <h1 className="text-[28px] md:text-[32px] lg:text-[56px] font-medium ">FLOOD RISK MAP</h1>
                <p className="typo-3xl mb-5" >Check for flood risk in your area</p>

                <div className="flex flex-col-reverse md:flex-row">
                    <div className="MapContainer h-120 md:w-[50%] md:h-165 rounded-sm border ">

                    </div>
                    <form className="md:w-[50%] flex flex-col items-center gap-5 ">
                        <div className="w-[90%] md:w-[50%] flex flex-col gap-5 items-start justify-center" >
                            <select name="country" id="location" className="w-full bg-white border border-[#296083] rounded-2xl py-1.75 px-5">
                                <option value="" disabled>Select Country</option>
                            </select>

                            <input type="text" placeholder="Region" className="w-full bg-white border border-[#296083] rounded-2xl py-1.75 px-5" />

                            <Button children={"Check flood warnings"} className="btb btn-accent btn-lg" />
                        </div>
                        
                        <RiskCard />
                    </form>
                </div>
            </div>
        </section>
     );
}
 
export default Map;
=======
const Map = () => {
  return <div>Map</div>;
};

export default Map;
>>>>>>> main
