import routes from "./routes";
import locationIcon from "../assets/svgIcons/location.svg";
import prepIcon from "../assets/svgIcons/prep.svg";
import usersIcon from "../assets/svgIcons/users.svg";
import localImg from "../assets/images/Local-img.jpg";
import checklistImg from "../assets/images/Local-img.jpg";
import communityImg from "../assets/images/Community-img.jpg";

export const ResourcesData = [
  {
    icon: locationIcon,
    title: "Local Resources",
    description:
      "Find out local resources and support services for flooding emergencies.",
    link: routes.main.localResources(),
  },
  {
    icon: prepIcon,
    title: "Emergency Prep",
    description:
      "Be ready for unanticipated floods with an emergency checklist and action steps if you get caught in an emergency.",
    link: routes.main.emergency(),
  },
  {
    icon: usersIcon,
    title: "Community Support",
    description:
      "Shared information, mutual aid, and local coordination before and after floods. ",
    link: routes.main.support(),
  },
];

export const ResourcessPage = [
  {
    image: localImg,
    title: "Local Resources",
    description:
      "Find out local resources and support services for flooding emergencies.",
    link: routes.main.localResources(),
  },
  {
    image: checklistImg,
    title: "Emergency Prep",
    description:
      "Be ready for unanticipated floods with an emergency checklist and action steps if you get caught in an emergency",
    link: routes.main.emergency(),
  },
  {
    image: communityImg,
    title: "Community Support",
    description:
      "Shared information, mutual aid, and local coordination before and after floods. ",
    link: routes.main.support(),
  },
];

export const emergData = {
  before: [
    {
      title: "Get an emergency kit ready",
      description: [
        "Safe drinking water",
        "Non-perishable food",
        "First aid supplies",
        "Flashlight + batteries",
        "Fully charged phone + power bank",
        "Important documents in waterproof bag",
        "Warm clothing",
      ],
    },
    {
      title: "Protect Your Home",
      description: [
        "Elevate valuables",
        "Clear drainage paths",
        "Identify safe routes to higher ground",
        "Store emergency contacts offline",
      ],
    },
    {
      title: "Family Preparedness",
      description: [
        "Set a meeting point",
        "Share evacuation plan",
        "Assign responsibilities",
      ],
    },
  ],

  after: [
    {
      title: "When a Flood Alert Is Issued",
      description: [
        "Monitor alerts in the app",
        "Charge devices",
        "Move essential items to higher ground",
        "Prepare to evacuate early",
        "Avoid flood-prone routes",
      ],
    },
  ],
};
