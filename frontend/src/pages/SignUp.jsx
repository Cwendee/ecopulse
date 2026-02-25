import { useState } from "react";
import { FormProvider, useForm } from "react-hook-form";
import FormInput from "../components/ReUsables/FormInput";
import Button from "../components/ReUsables/Button";
import Modal from "../components/ReUsables/Modal";
import { useNavigate } from "react-router-dom";
import routes from "../constants/routes";
import { useCountries, useRegions } from "../hooks/APIHooks";

const SignUp = () => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [modalType, setModalType] = useState(null);
  const navigate = useNavigate();

  const baseUrl = import.meta.env.VITE_BASE_URL;

  const form = useForm({
    mode: "onChange",
    defaultValues: {
      email: "",
      location: "",
      region: "",
      severe_alerts: true,
      early_alerts: true,
      preparedness_reminders: false,
      email_delivery: true,
      in_app_delivery: false,
      browser_delivery: false,
    },
  });

  const {
    watch,
    reset,
    handleSubmit,
    formState: { isValid },
  } = form;
  const selectedCountry = watch("country");

  const { data: countryData, isLoading: loadingCountries } = useCountries();
  const { data: regionData, isLoading: loadingRegions } =
    useRegions(selectedCountry);

  const onSubmit = async (data) => {
    setIsSubmitting(true);

    try {
      const response = await fetch(`${baseUrl}/subscribe`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) throw new Error("Network response not ok");

      setModalType("success");
      reset();
    } catch (error) {
      console.error("Submission error:", error);
      setModalType("error");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section className="site-container space-y-8">
      <div className="space-y-2">
        <h1 className="typo-4xl font-bold">Flood Alert Notifications</h1>
        <p className="typo-2xl">
          Sign up with your email only and receive timely flood warnings.
        </p>
      </div>

      <FormProvider {...form}>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <FormInput
            type="email"
            required
            placeholder="example@gmail.com"
            label="Email Address"
            name="email"
          />
          <div className="space-y-8">
            <div className="space-y-1">
              <label className="form-label typo-2xl">Country</label>
              <select
                value={selectedCountry}
                {...form.register("country", { required: true })}
                className="form-input"
              >
                <option value="">
                  {loadingCountries ? "Loading..." : "Select Country"}
                </option>
                {countryData?.countries?.map((country) => (
                  <option key={country.code} value={country.code}>
                    {country.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="space-y-1">
              <select
                {...form.register("region_id", { required: true })}
                className="form-input"
                disabled={!selectedCountry}
              >
                <option value="">
                  {loadingRegions ? "Fetching regions..." : "Select Region"}
                </option>
                {regionData?.regions?.map((reg) => (
                  <option key={reg.region_id} value={reg.region_id}>
                    {reg.region_name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="space-y-4">
            <div className="space-y-4">
              <h2 className="typo-2xl">Alert Preferences</h2>
              <p className="typo-base">
                Let us know what flood alert notifications you would like to
                receive. Select all which apply.
              </p>

              {[
                { label: "Severe flood warnings", value: "severe_flood" },
                {
                  label: "Early risk alerts (rainfall + river levels)",
                  value: "early_risk",
                },
                { label: "Preparedness reminders", value: "preparedness" },
              ].map((item) => (
                <label
                  key={item.value}
                  className="flex items-center gap-3 text-xl"
                >
                  <input
                    type="checkbox"
                    value={item.value}
                    className="w-7 h-7 border-2 border-[#008B8B]"
                  />
                  {item.label}
                </label>
              ))}
            </div>
            <div className="space-y-4">
              <h2 className="typo-2xl">Delivery</h2>
              <p className="typo-base">
                How would you like to receive notifications? Select all which
                apply.
              </p>

              {[
                { label: "Email alerts only", value: "email" },
                { label: "In-app alerts", value: "in_app" },
                { label: "Browser notifications", value: "browser" },
              ].map((item) => (
                <label
                  key={item.value}
                  className="flex items-center gap-3 text-xl"
                >
                  <input
                    type="checkbox"
                    value={item.value}
                    className="w-7 h-7 border-2 outline-[#008B8B]"
                  />
                  {item.label}
                </label>
              ))}
            </div>
          </div>
          <Button
            className="btn btn-primary btn-md"
            type="submit"
            disabled={!isValid || isSubmitting}
          >
            {isSubmitting ? "Submitting..." : "Submit"}
          </Button>
        </form>
      </FormProvider>

      <Modal
        title="You’re ready to receive flood alerts."
        opened={modalType === "success"}
        onClose={() => setModalType(null)}
        image={"successGif"}
      >
        <Button
          type="button"
          size="lg"
          className="btn btn-primary btn-md"
          onClick={() => navigate(routes.main.home())}
        >
          Continue to Home
        </Button>
      </Modal>
      <Modal
        title="Flood alert subscription failed."
        opened={modalType === "error"}
        onClose={() => setModalType(null)}
        image={"warningGif"}
      >
        <p className="text-center typo-lg">
          We couldn’t process your subscription. Please try again.
        </p>
        <div className="space-x-3">
          <Button
            type="button"
            size="lg"
            className="btn btn-primary btn-md"
            onClick={() => navigate(routes.main.subscribe())}
          >
            Try Again
          </Button>

          <Button
            type="button"
            size="lg"
            className="btn btn-accent btn-md"
            onClick={() => navigate(routes.main.home())}
          >
            Continue to Home
          </Button>
        </div>
      </Modal>
    </section>
  );
};

export default SignUp;
