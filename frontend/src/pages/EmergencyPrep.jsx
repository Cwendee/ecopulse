import emerPage from "../assets/images/emer.jpg";
import Button from "../components/ReUsables/Button";
import { emergData } from "../constants";
import { GoCheckbox } from "react-icons/go";
import { IoMdDownload } from "react-icons/io";

const EmergencyPrep = () => {
  return (
    <section className="site-container space-y-6">
      <h1 className="typo-4xl">Emergency Preparedness and Guidance</h1>
      <section>
        <img src={emerPage} alt="Two guys" />
      </section>
      <section className="bg-[#C6E2E8] rounded-xl py-6.5 px-3 md:px-6">
        <h1 className="font-medium text-[40px] x:text-[56px]">Before</h1>
        <div className="flex flex-col gap-y-10">
          {emergData.before.map((data, index) => (
            <div key={index}>
              <span className="flex items-center space-x-2">
                <GoCheckbox size={24} />

                <p className="typo-2xl">{data.title}</p>
              </span>
              <ul className="list-disc pl-6">
                {data.description.map((item, i) => (
                  <li key={i} className="text-base md:text-xl font-medium">
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>
      <div className="bg-[#C6E2E8] rounded-xl py-6.5 px-3 md:px-6">
        {emergData.after.map((data, index) => (
          <div key={index}>
            <p className="typo-2xl">{data.title}</p>

            <ul className="list-disc pl-6">
              {data.description.map((item, i) => (
                <li key={i} className="text-base md:text-xl font-medium">
                  {item}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
      <div className="flex flex-col mx-auto text-center rounded-md border-[2.2px] border-[#008B8B] py-2 px-4 w-full max-w-151 space-y-8.5">
        <p className="typo-xl w-full max-w-143">
          Download our emergency checklist to make sure you’re ready for
          unexpected flood alerts.
        </p>
        <div className="mx-auto">
          <Button
            className="btn btn-primary btn-md"
            rightSection={<IoMdDownload />}
          >
            download here
          </Button>
        </div>
      </div>
    </section>
  );
};

export default EmergencyPrep;
