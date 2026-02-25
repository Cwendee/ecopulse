import routes from "./routes";
import locationIcon from "../assets/svgIcons/location.svg";
import prepIcon from "../assets/svgIcons/prep.svg";
import usersIcon from "../assets/svgIcons/users.svg";
import localImg from "../assets/images/Local-img.jpg";
import checklistImg from "../assets/images/Local-img.jpg";
import communityImg from "../assets/images/Community-img.jpg";
import Low from "../assets/svgIcons/low.svg?react";
import Moderate from "../assets/svgIcons/moderate.svg?react";
import High from "../assets/svgIcons/high.svg?react";

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

export const headerNavigation = [
  {
    title: "Home",
    link: routes.main.home(),
  },
  {
    title: "Map",
    link: routes.main.map(),
  },
  {
    title: "Resources",
    link: routes.main.resources(),
  },
  {
    title: "About Us",
    link: routes.main.about(),
  },
];

export const aboutUs = [
  {
    title: "Our Mission",
    content: "At EcoPulse, we believe that being prepared can make all the difference. Our mission is to share clear, easy-to-understand flood-risk insights that help residents and small businesses feel informed, confident, and ready. By giving people simple, location-based guidance, we aim to make preparedness a natural and empowering part of everyday life—long before any emergency comes along.",
    background: "bg-[#63B7B9]",
  },
  {
    title: "Our Vision",
    content: "We imagine a world where people feel safe, supported, and ready—no matter the weather. A world where preparedness is part of everyday life, and where everyone has the guidance they need to protect their homes, their dreams, and their future.",
    background: "bg-[#C6E2E8]",
  },
  {
    title: "Our Values",
    content: "At EcoPulse, we value clarity, trust, and community. We believe everyone deserves simple, reliable information that helps them stay safe. We are committed to transparency, compassion, and continuous learning—so we can support people with the guidance they need, when they need it most. Our values are rooted in care and responsibility. We listen to communities, prioritize ease of use, and strive to turn complex data into guidance that supports safety, confidence, and resilience for all.",
    background: "bg-[#64A5CE]",
  },
]

export const pages = {
  home: routes.main.home(),
  resources: routes.main.resources(),
  about: routes.main.about(),
  contact: routes.main.contact(),
  faq: routes.main.faq(),
  support: routes.main.support(),
  emergency: routes.main.emergency(),
  localResources: routes.main.localResources(),
  map: routes.main.map(),
  signup: routes.main.signup(),
  chat: routes.main.chatbot(),
}

export const Risk = {
  low:{
    icon: Low,
    title: "Low Risk - Stay Ready",
    content: "Flooding unlikely at this time. No immediate action needed, but review your plan and stay informed.",
    firstButton: "Enable alerts",
    secondButton: "View resources",
    bg: "bg-[#4CBB17]",
    border: "border-5 border-[#4CBB17]",
    firstLink: routes.main.signup(),
    secondLink: routes.main.resources(),
  },

  moderate:{
    icon: Moderate,
    title: "Moderate Risk - Prepare Now",
    content: "Flooding possible in low lying areas. Take precautionary steps to reduce damage and stay ready for updates",
    firstButton: "Prepare for flooding",
    secondButton: "View emergency preparation",
    bg: "bg-[#FE5A1D]",
    border: "border-5 border-[#FE5A1D]",
    firstLink: routes.main.emergency(),
    secondLink: routes.main.emergency(),
  },

  high:{
    icon: High,
    title: "High Risk - Take Action Now",
    content: "Flooding expected in your area within 24 hours.  Take protective measures. Avoid floodwater and follow local guidance. ",
    firstButton: "Emergency Prep",
    secondButton: "View local resources",
    bg: "bg-[#CE2029]",
    border: "border-5 border-[#CE2029]",
    firstLink: routes.main.emergency(),
    secondLink: routes.main.localResources(),
  }
}