import routes from "./routes";
import locationIcon from "../assets/svgIcons/location.svg";
import prepIcon from "../assets/svgIcons/prep.svg";
import usersIcon from "../assets/svgIcons/users.svg";



export const ResourcesData = [
  {
    icon: locationIcon,
    title: "Local Resources",
    description:
      "Find out local resources and support services for flooding emergencies.",
    link: routes.main.resources,
  },
  {
    icon: prepIcon,
    title: "Emergency Prep",
    description:
      "Be ready for unanticipated floods with an emergency checklist and action steps if you get caught in an emergency.",
  },
  {
    icon: usersIcon,
    title: "Community Support",
    description:
      "Shared information, mutual aid, and local coordination before and after floods. ",
  },
];
