import sosImg from "../assets/images/emojione-v1_sos-button.png";

const LocalPage = () => {
  return (
    <section className="site-container space-y-6">
      <h1 className="typo-4xl">Local Resources</h1>
      <section className="space-y-8">
        <div className="flex flex-col-reverse md:flex-row justify-between items-center border-[2.2px] border-[#296083] rounded-xl p-3 bg-[#C6E2E8]">
          <div>
            <h2 className="typo-3xl">Local Emergency Contacts</h2>
            <div>
              {[
                {
                  text: "Emergency services",
                  phone: "0000",
                },
                {
                  text: "Red cross",
                  phone: "+000 0000",
                },
                {
                  text: "Fire Station",
                  phone: "+000 0000",
                },
              ].map((data, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between typo-xl"
                >
                  <h4>{data.text}</h4>
                  <h4>{data.phone}</h4>
                </div>
              ))}
            </div>
          </div>

          <img src={sosImg} alt="SOS image" />
        </div>
        <div>
          <h2 className="typo-3xl">Local Shelters</h2>
          <div>
            {[
              {
                text: "Hillcrest Community Refuge",
                phone: "+000 0000",
              },
              {
                text: "Red cross",
                phone: "+000 0000",
              },
              {
                text: "Floodline Support Hub",
                phone: "+000 0000",
              },
            ].map((data, index) => (
              <div
                key={index}
                className="flex items-center justify-between typo-xl"
              >
                <h4>{data.text}</h4>
                <h4>{data.phone}</h4>
              </div>
            ))}
          </div>
        </div>
      </section>
    </section>
  );
};

export default LocalPage;
