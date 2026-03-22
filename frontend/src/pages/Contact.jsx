import { teamData } from "../constants";
import { GoDash } from "react-icons/go";

const Contact = () => {
  return (
    <section className="site-container space-y-6">
      <h1 className="typo-4xl">Contact Us</h1>
      <p className="typo-3xl">
        Contact the Impact Collective team that worked on Eco Pulse
      </p>
      <div className="space-y-6">
        {teamData.map((item) => (
          <details className="group">
            <summary className="typo-3xl py-3 px-4 bg-[#C6E2E8] rounded-xl flex justify-between items-center cursor-pointer">
              <span>{item.title}</span>

              <span className="text-2xl font-bold">
                <GoDash />
              </span>
            </summary>
            <ul className="list-disc my-4 pl-10 py-3 bg-[#C6E2E8] rounded-xl">
              {item.users.map((item, i) => (
                <li key={i} className="text-base md:text-[22px] font-medium">
                  {item}
                </li>
              ))}
            </ul>
          </details>
        ))}
      </div>
    </section>
  );
};

export default Contact;
