import { useEffect, useState } from "react";
import commPage from "../assets/images/comm-page.jpg";

const CommunityPage = () => {
  const launchDate = new Date("2026-04-15T00:00:00");
  const [timeLeft, setTimeLeft] = useState(getTimeRemaining());

  function getTimeRemaining() {
    const total = launchDate - new Date();

    const days = Math.floor(total / (1000 * 60 * 60 * 24));
    const hours = Math.floor((total / (1000 * 60 * 60)) % 24);
    const minutes = Math.floor((total / 1000 / 60) % 60);
    const seconds = Math.floor((total / 1000) % 60);

    return { total, days, hours, minutes, seconds };
  }

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft(getTimeRemaining());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  return (
    <section className="site-container space-y-6">
      <h1 className="typo-4xl">Community Support</h1>

      <section>
        <img src={commPage} alt="" className="w-full rounded-xl" />
      </section>

      <div className="space-y-2 md:space-y-4 text-center">
        <h1 className="typo-2xl">Coming Soon</h1>

        <p className="typo-lg max-w-lg mx-auto">
          Support Is On The Way. We’re putting the finishing touches on our new
          website and building a dedicated space for community resources and
          support. Check back soon.
        </p>

        <div className="flex justify-center gap-1 md:gap-4 mt-6">
          {["days", "hours", "minutes", "seconds"].map((unit) => (
            <div
              key={unit}
              className="bg-[#296083] shadow-md rounded-lg text-white px-2 md:px-4 py-3 min-w-17.5"
            >
              <p className="text-lg md:text-xl font-bold">{timeLeft[unit] ?? "0"}</p>
              <p className="text-xs uppercase">{unit}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default CommunityPage;
