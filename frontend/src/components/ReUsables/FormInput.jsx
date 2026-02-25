import { useFormContext } from "react-hook-form";
import { cn } from "../../lib/utilities";

const FormInput = ({
  label,
  type = "text",
  required,
  validation,
  name,
  id = name,
}) => {
  const {
    register,
    formState: { errors },
  } = useFormContext();

  const error = errors[name]?.message?.toString();

  const isArea = type === "textarea";

  const Input = isArea ? "textarea" : "input";

  return (
    <div className={cn("form-group", error && "error")}>
      <div>
        <label
          htmlFor={id}
          className={cn(
            `
          form-label 
          typo-2xl
            `,
            isArea
              ? "top-6"
              : `          
          peer-focus:top-4
          peer-placeholder-shown:top-1/2
          peer-placeholder-shown:-translate-y-1/2
          peer-not-placeholder-shown:top-4
          `,
          )}
        >
          {label}
          {/* {required ? <span className="asterick"> *</span> : null} */}
        </label>
        <Input
          id={id}
          type={type}
          {...register(name, {
            ...validation,
            required: required ? `${label} is required` : false,
          })}
          placeholder=""
          className={cn(
            `
          peer
          form-input
          focus:outline-none
          resize-none
            `,
            isArea && "h-43.25 pt-12",
          )}
        />
      </div>

      {error ? (
        <div>
          <p className="text-red break-all">{error}</p>
        </div>
      ) : null}
    </div>
  );
};

export default FormInput;
