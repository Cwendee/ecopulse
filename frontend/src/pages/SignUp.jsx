import { useEffect, useState } from "react";
import Button from "../components/ReUsables/Button";
import { useNavigate } from "react-router-dom";
import { FormProvider, useForm } from "react-hook-form";
import Modal from "../components/ReUsables/Modal";
import routes from "../constants/routes";
import { useCountries, useRegions } from "../hooks/APIHooks";

const SignUp = ({ onClose, defaultEmail }) => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [modalType, setModalType] = useState(null);
  const navigate = useNavigate();

  const baseUrl = import.meta.env.VITE_BASE_URL;

  const form = useForm({
    mode: "onChange",
    defaultValues: {
      email: defaultEmail || "",
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

  useEffect(() => {
    if (defaultEmail) {
      reset({
        email: defaultEmail,
        location: "",
        region: "",
        severe_alerts: true,
        early_alerts: true,
        preparedness_reminders: false,
        email_delivery: true,
        in_app_delivery: false,
        browser_delivery: false,
      });
    }
  }, [defaultEmail, reset]);
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
    <div className="space-y-3 lg:space-y-8">
      <p className="text-2xl font-medium lg:typo-2xl text-white text-start">
        Subscribe for timely flood warnings.
      </p>

      <FormProvider {...form}>
        <form
          onSubmit={handleSubmit(onSubmit)}
          className="space-y-2 lg:space-y-6 text-white text-start"
        >
          <div className="space-y-1">
            <label className="form-label text-2xl font-medium lg:typo-2xl text-white">
              Email
            </label>{" "}
            <input
              type="email"
              {...form.register("email", { required: true })}
              required
              placeholder="example@gmail.com"
              label="Email Address"
              name="email"
              className="w-full border-[1.5px] border-white rounded-2xl h-13.5 px-4"
            />
          </div>

          <div className="space-y-2 lg:space-y-8">
            <div className="space-y-1">
              <label className="form-label text-2xl font-medium lg:typo-2xl text-white">
                Country
              </label>
              <select
                value={selectedCountry}
                {...form.register("country", { required: true })}
                className="form-input border-white"
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
                className="form-input border-white"
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

          <div className="space-y-2 lg:space-y-4">
            <div className="space-y-4">
              <h2 className="text-2xl font-medium lg:typo-2xl">
                Alert Preferences
              </h2>
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
                  className="flex items-center gap-3 text-sm lg:text-xl"
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
            <div className="space-y-2 lg:space-y-4">
              <h2 className="text-2xl font-medium lg:typo-2xl">Delivery</h2>
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
                  className="flex items-center gap-3 text-sm lg:text-xl"
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
            className="btn btn-accent text-white btn-md"
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
        bgColor="white"
      >
        <Button
          type="button"
          size="lg"
          className="btn btn-primary btn-md"
          onClick={onClose}
        >
          Continue to Home
        </Button>
      </Modal>
      <Modal
        title="Flood alert subscription failed."
        opened={modalType === "error"}
        onClose={() => setModalType(null)}
        image={"warningGif"}
        bgColor="#E34234"
      >
        <p className="text-center typo-lg text-white">
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
    </div>
  );
};

export default SignUp;
