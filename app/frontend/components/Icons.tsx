import React from 'react';

// Fix: Define props with an interface for better type inference.
interface IconProps {
  children: React.ReactNode;
  className?: string;
}

const Icon = ({ children, className = '' }: IconProps) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="currentColor"
    className={`w-6 h-6 ${className}`}
    style={{ width: '1.5rem', height: '1.5rem' }}
  >
    {children}
  </svg>
);

// Fix: Define a reusable props interface for specialized icons.
interface SpecificIconProps {
  className?: string;
}

export const DashboardIcon = (props: SpecificIconProps) => (
  <Icon {...props}>
    <path fillRule="evenodd" d="M3.75 3A1.75 1.75 0 0 0 2 4.75v14.5A1.75 1.75 0 0 0 3.75 21h16.5A1.75 1.75 0 0 0 22 19.25V4.75A1.75 1.75 0 0 0 20.25 3H3.75ZM3.5 10.75v8.5a.25.25 0 0 0 .25.25h5a.25.25 0 0 0 .25-.25v-8.5H3.5ZM9.25 4.5a.25.25 0 0 0-.25.25v5.5h11.25V4.75a.25.25 0 0 0-.25-.25H9.25ZM3.5 4.75a.25.25 0 0 1 .25-.25h5a.25.25 0 0 1 .25.25v5.5H3.5v-5.5Zm10.5 6v8.5a.25.25 0 0 0 .25.25h5a.25.25 0 0 0 .25-.25v-8.5H14Z" clipRule="evenodd" />
  </Icon>
);

export const MapIcon = (props: SpecificIconProps) => (
  <Icon {...props}>
    <path fillRule="evenodd" d="m11.54 22.351.07.04.028.016a.76.76 0 0 0 .723 0l.028-.015.071-.041a2.25 2.25 0 0 0 2.16-2.16l-.04-.071a.76.76 0 0 0 0-.722l.04-.071a2.25 2.25 0 0 0-2.16-2.16l-.071.04a.76.76 0 0 0-.722 0l-.071-.04a2.25 2.25 0 0 0-2.16 2.16l.04.071a.76.76 0 0 0 0 .722l-.04.071a2.25 2.25 0 0 0 2.16 2.16ZM12 18a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z" clipRule="evenodd" />
    <path d="M11.94 1.575a1.5 1.5 0 0 1 .12.188l6 10.5a1.5 1.5 0 0 1-1.32 2.237h-3.34a1.5 1.5 0 0 1-1.48-1.075a4.5 4.5 0 0 0-4.66-3.413a1.5 1.5 0 0 1-1.04-2.734l3-4.5a1.5 1.5 0 0 1 2.72-.187Z" />
  </Icon>
);


// Fix: Pass props via spread to avoid potential TS inference issue with children prop.
export const ThermometerIcon = (props: SpecificIconProps) => (
  <Icon {...props}>
    <path d="M12 1.75a2.25 2.25 0 0 0-2.25 2.25v7.622a4.5 4.5 0 1 0 4.5 0V4A2.25 2.25 0 0 0 12 1.75ZM12 4a.75.75 0 0 1 .75.75v6.19a4.502 4.502 0 0 0-1.5 0V4.75A.75.75 0 0 1 12 4Zm0 15a3 3 0 0 1-1-5.815V15a1 1 0 1 1-2 0v-1.815a3 3 0 1 1 3 3Z" />
  </Icon>
);

// Fix: Pass props via spread to avoid potential TS inference issue with children prop.
export const StepsIcon = (props: SpecificIconProps) => (
    <Icon {...props}>
        <path fillRule="evenodd" d="M12.25 21.75a.75.75 0 0 0 .75-.75V16.5a.75.75 0 0 0-1.5 0v4.5a.75.75 0 0 0 .75.75ZM8.25 18.75a.75.75 0 0 1-.75.75h-1.5a.75.75 0 0 1 0-1.5h1.5a.75.75 0 0 1 .75.75Zm6 0a.75.75 0 0 1-.75.75h-1.5a.75.75 0 0 1 0-1.5h1.5a.75.75 0 0 1 .75.75ZM9 15.75a.75.75 0 0 0 .75-.75v-4.5a.75.75 0 0 0-1.5 0v4.5a.75.75 0 0 0 .75.75Zm6 0a.75.75 0 0 0 .75-.75v-4.5a.75.75 0 0 0-1.5 0v4.5a.75.75 0 0 0 .75.75Zm-3-8.25a.75.75 0 0 1-.75.75h-1.5a.75.75 0 0 1 0-1.5h1.5a.75.75 0 0 1 .75.75Zm-3 3a.75.75 0 0 0 .75-.75V6a.75.75 0 0 0-1.5 0v4.5a.75.75 0 0 0 .75.75Zm6 0a.75.75 0 0 0 .75-.75V6a.75.75 0 0 0-1.5 0v4.5a.75.75 0 0 0 .75.75Zm2.25-5.25a.75.75 0 0 1-.75.75h-1.5a.75.75 0 0 1 0-1.5h1.5a.75.75 0 0 1 .75.75ZM8.25 5.25a.75.75 0 0 1-.75.75h-1.5a.75.75 0 0 1 0-1.5h1.5a.75.75 0 0 1 .75.75ZM12 3a.75.75 0 0 0 .75-.75V1.5a.75.75 0 0 0-1.5 0V2.25A.75.75 0 0 0 12 3Z" clipRule="evenodd" />
    </Icon>
);

// Fix: Pass props via spread to avoid potential TS inference issue with children prop.
export const LocationIcon = (props: SpecificIconProps) => (
    <Icon {...props}>
        <path fillRule="evenodd" d="M12 21.75c-4.142 0-7.5-3.358-7.5-7.5s3.358-7.5 7.5-7.5 7.5 3.358 7.5 7.5-3.358 7.5-7.5 7.5ZM12 1.5a.75.75 0 0 1 .75.75v1.5a.75.75 0 0 1-1.5 0V2.25a.75.75 0 0 1 .75-.75Zm0 21a.75.75 0 0 1-.75-.75v-1.5a.75.75 0 0 1 1.5 0v1.5a.75.75 0 0 1-.75-.75Zm-9-9a.75.75 0 0 1-.75.75H.75a.75.75 0 0 1 0-1.5h1.5a.75.75 0 0 1 .75.75Zm21 0a.75.75 0 0 1-.75.75h-1.5a.75.75 0 0 1 0-1.5h1.5a.75.75 0 0 1 .75.75Z" clipRule="evenodd" />
    </Icon>
);

// Fix: Pass props via spread to avoid potential TS inference issue with children prop.
export const SendIcon = (props: SpecificIconProps) => (
    <Icon {...props}>
        <path d="M3.478 2.405a.75.75 0 0 0-.926.94l2.432 7.905H13.5a.75.75 0 0 1 0 1.5H4.984l-2.432 7.905a.75.75 0 0 0 .926.94 60.519 60.519 0 0 0 18.445-8.986.75.75 0 0 0 0-1.218A60.517 60.517 0 0 0 3.478 2.405Z" />
    </Icon>
);

// Fix: Pass props via spread to avoid potential TS inference issue with children prop.
export const CloseIcon = (props: SpecificIconProps) => (
    <Icon {...props}>
        <path fillRule="evenodd" d="M5.47 5.47a.75.75 0 0 1 1.06 0L12 10.94l5.47-5.47a.75.75 0 1 1 1.06 1.06L13.06 12l5.47 5.47a.75.75 0 1 1-1.06 1.06L12 13.06l-5.47 5.47a.75.75 0 0 1-1.06-1.06L10.94 12 5.47 6.53a.75.75 0 0 1 0-1.06Z" clipRule="evenodd" />
    </Icon>
);

// Fix: Pass props via spread to avoid potential TS inference issue with children prop.
export const ChatBotIcon = (props: SpecificIconProps) => (
    <Icon {...props}>
      <path d="M15.5 2.5a1 1 0 0 0-1.5 1.25 5.25 5.25 0 0 1 0 9.5 1 1 0 1 0 1.5 1.25 6.75 6.75 0 0 0 0-12Z" />
      <path d="M8.5 2.5a1 1 0 0 1 1.5 1.25 5.25 5.25 0 0 0 0 9.5 1 1 0 1 1-1.5 1.25 6.75 6.75 0 0 1 0-12Z" />
      <path fillRule="evenodd" d="M12 4a8 8 0 0 0-8 8c0 2.905 1.573 5.53 4 6.932V12.5a4 4 0 1 1 8 0v6.432c2.427-1.402 4-4.027 4-6.932a8 8 0 0 0-8-8Zm-3 10a1 1 0 1 0 0-2 1 1 0 0 0 0 2Zm6 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2Z" clipRule="evenodd" />
    </Icon>
);
  
// Fix: Pass props via spread to avoid potential TS inference issue with children prop.
export const ChevronLeftIcon = (props: SpecificIconProps) => (
    <Icon {...props}>
      <path fillRule="evenodd" d="M15.707 4.293a1 1 0 0 1 0 1.414L9.414 12l6.293 6.293a1 1 0 0 1-1.414 1.414l-7-7a1 1 0 0 1 0-1.414l7-7a1 1 0 0 1 1.414 0Z" clipRule="evenodd" />
    </Icon>
);
  
// Fix: Pass props via spread to avoid potential TS inference issue with children prop.
export const ChevronRightIcon = (props: SpecificIconProps) => (
    <Icon {...props}>
      <path fillRule="evenodd" d="M8.293 19.707a1 1 0 0 1 0-1.414L14.586 12 8.293 5.707a1 1 0 0 1 1.414-1.414l7 7a1 1 0 0 1 0 1.414l-7 7a1 1 0 0 1-1.414 0Z" clipRule="evenodd" />
    </Icon>
);

// Fix: Pass props via spread to avoid potential TS inference issue with children prop.
export const ChevronUpIcon = (props: SpecificIconProps) => (
    <Icon {...props}>
        <path fillRule="evenodd" d="M11.47 7.72a.75.75 0 0 1 1.06 0l7.5 7.5a.75.75 0 1 1-1.06 1.06L12 9.31l-6.97 6.97a.75.75 0 0 1-1.06-1.06l7.5-7.5Z" clipRule="evenodd" />
    </Icon>
);

// Fix: Pass props via spread to avoid potential TS inference issue with children prop.
export const ChevronDownIcon = (props: SpecificIconProps) => (
    <Icon {...props}>
        <path fillRule="evenodd" d="M12.53 16.28a.75.75 0 0 1-1.06 0l-7.5-7.5a.75.75 0 0 1 1.06-1.06L12 14.69l6.97-6.97a.75.75 0 1 1 1.06 1.06l-7.5 7.5Z" clipRule="evenodd" />
    </Icon>
);

// Fix: Pass props via spread to avoid potential TS inference issue with children prop.
export const MinusIcon = (props: SpecificIconProps) => (
    <Icon {...props}>
      <path fillRule="evenodd" d="M5.25 12a.75.75 0 0 1 .75-.75h12a.75.75 0 0 1 0 1.5H6a.75.75 0 0 1-.75-.75Z" clipRule="evenodd" />
    </Icon>
);

// Fix: Pass props via spread to avoid potential TS inference issue with children prop.
export const CowIcon = (props: SpecificIconProps) => (
    <Icon {...props}>
      <path fillRule="evenodd" d="M20.25 12a.75.75 0 0 0-.75-.75H18a.75.75 0 0 1-.75-.75V9a2.25 2.25 0 0 0-2.25-2.25h-1.5V5.25a.75.75 0 0 0-1.5 0v1.5h-1.5V5.25a.75.75 0 0 0-1.5 0v1.5H7.5A2.25 2.25 0 0 0 5.25 9v1.5a.75.75 0 0 1-.75.75H3.75a.75.75 0 0 0 0 1.5h.75a.75.75 0 0 1 .75.75v3A2.25 2.25 0 0 0 7.5 19.5h9A2.25 2.25 0 0 0 18.75 17.25v-3a.75.75 0 0 1 .75-.75h.75a.75.75 0 0 0 0-1.5ZM17.25 15v2.25a.75.75 0 0 1-.75.75h-9a.75.75 0 0 1-.75-.75V15h10.5Z" clipRule="evenodd" />
    </Icon>
);
  
// Fix: Pass props via spread to avoid potential TS inference issue with children prop.
export const BreedIcon = (props: SpecificIconProps) => (
    <Icon {...props}>
      <path fillRule="evenodd" d="M6.28 5.22a.75.75 0 0 1 0 1.06l-1.47 1.47a.75.75 0 1 1-1.06-1.06L5.22 5.22a.75.75 0 0 1 1.06 0ZM7.72 6.66a.75.75 0 0 0 0-1.06L6.25 4.13a.75.75 0 0 0-1.06 1.06l1.47 1.47a.75.75 0 0 0 1.06 0ZM17.78 13.28a.75.75 0 0 1-1.06 0l-1.47-1.47a.75.75 0 0 1 1.06-1.06l1.47 1.47a.75.75 0 0 1 0 1.06Zm1.44-1.44a.75.75 0 0 0-1.06 0l-1.47 1.47a.75.75 0 1 0 1.06 1.06l1.47-1.47a.75.75 0 0 0 0-1.06ZM17.25 7.5a.75.75 0 0 1-.75.75A5.25 5.25 0 0 1 6.75 13.5a.75.75 0 0 1 0-1.5A3.75 3.75 0 0 0 10.5 8.25a.75.75 0 0 1 .75-.75A5.25 5.25 0 0 1 16.5 2.25a.75.75 0 0 1 1.5 0A6.75 6.75 0 0 0 11.25 9a.75.75 0 0 1-1.5 0A5.25 5.25 0 0 1 15 3.75a.75.75 0 0 1 .75.75A3.75 3.75 0 0 0 19.5 8.25a.75.75 0 0 1 0 1.5A5.25 5.25 0 0 1 14.25 15a.75.75 0 0 1-.75.75A6.75 6.75 0 0 0 21 9a.75.75 0 0 1-1.5 0A5.25 5.25 0 0 1 14.25 3.75a.75.75 0 0 1 0-1.5A6.75 6.75 0 0 0 7.5 9a.75.75 0 0 1-1.5 0A5.25 5.25 0 0 1 1.25 3.75a.75.75 0 0 1 1.5 0A3.75 3.75 0 0 0 6.5 7.5a.75.75 0 0 1 0 1.5A5.25 5.25 0 0 1 1.25 13.5a.75.75 0 0 1-1.5 0A6.75 6.75 0 0 0 6.5 16.5a.75.75 0 0 1 0-1.5A5.25 5.25 0 0 1 11.25 9.75a.75.75 0 0 1 1.5 0A3.75 3.75 0 0 0 9 15.75a.75.75 0 0 1 0 1.5A5.25 5.25 0 0 1 3.75 21a.75.75 0 0 1-1.5 0A6.75 6.75 0 0 0 9 15.75a.75.75 0 0 1 1.5 0 5.25 5.25 0 0 1 4.25 5.25.75.75 0 0 1-1.5 0A3.75 3.75 0 0 0 9.5 17.25a.75.75 0 0 1 0-1.5A5.25 5.25 0 0 1 14.25 21a.75.75 0 0 1-1.5 0 3.75 3.75 0 0 0-3.75-3.75.75.75 0 0 1 0-1.5Z" clipRule="evenodd" />
    </Icon>
);
  
// Fix: Pass props via spread to avoid potential TS inference issue with children prop.
export const AgeIcon = (props: SpecificIconProps) => (
    <Icon {...props}>
      <path fillRule="evenodd" d="M6 3.75A2.25 2.25 0 0 0 3.75 6v12A2.25 2.25 0 0 0 6 20.25h12A2.25 2.25 0 0 0 20.25 18V6A2.25 2.25 0 0 0 18 3.75H6ZM18 2.25a.75.75 0 0 1 .75.75v.75h-3a.75.75 0 0 1 0-1.5h3ZM8.25 3h3a.75.75 0 0 1 0 1.5h-3a.75.75 0 0 1 0-1.5ZM5.25 3a.75.75 0 0 1 .75-.75h.75a.75.75 0 0 1 0 1.5h-.75a.75.75 0 0 1-.75-.75Zm9.75 6a.75.75 0 0 0-1.5 0v6a.75.75 0 0 0 1.5 0V9Zm-3.75 0a.75.75 0 0 0-1.5 0v6a.75.75 0 0 0 1.5 0V9Zm-3.75 0a.75.75 0 0 0-1.5 0v6a.75.75 0 0 0 1.5 0V9Z" clipRule="evenodd" />
    </Icon>
);
  
// Fix: Pass props via spread to avoid potential TS inference issue with children prop.
export const WeightIcon = (props: SpecificIconProps) => (
    <Icon {...props}>
      <path fillRule="evenodd" d="M12 1.5a.75.75 0 0 1 .75.75v1.313c3.27.155 5.869 2.11 7.233 4.887a.75.75 0 0 1-1.316.702c-1.223-2.52-3.52-4.152-6.167-4.152s-4.944 1.632-6.167 4.152a.75.75 0 1 1-1.316-.702C5.381 5.673 7.98 3.718 11.25 3.563V2.25a.75.75 0 0 1-.75-.75ZM2.25 12a.75.75 0 0 1 .75-.75h18a.75.75 0 0 1 0 1.5H3a.75.75 0 0 1-.75-.75Zm0 3.75a.75.75 0 0 1 .75-.75h18a.75.75 0 0 1 0 1.5H3a.75.75 0 0 1-.75-.75Zm1.22-8.52a.75.75 0 0 0-1.06.04l-1.5 1.75a.75.75 0 1 0 1.12 1.02l1.5-1.75a.75.75 0 0 0-.06-1.06Zm19.66 0a.75.75 0 0 1-.06 1.06l-1.5 1.75a.75.75 0 1 1-1.12-1.02l1.5-1.75a.75.75 0 0 1 1.18-.04ZM12 17.25a.75.75 0 0 1 .75.75v3.75a.75.75 0 0 1-1.5 0V18a.75.75 0 0 1 .75-.75Z" clipRule="evenodd" />
    </Icon>
);

// Fix: Pass props via spread to avoid potential TS inference issue with children prop.
export const TagIcon = (props: SpecificIconProps) => (
    <Icon {...props}>
      <path fillRule="evenodd" d="M4.5 3A1.5 1.5 0 0 0 3 4.5v5.379a1.5 1.5 0 0 0 .44 1.06l7.5 7.5a1.5 1.5 0 0 0 2.12 0l5.38-5.38a1.5 1.5 0 0 0 0-2.12l-7.5-7.5A1.5 1.5 0 0 0 9.879 3H4.5ZM6 6.75A.75.75 0 1 0 6 5.25a.75.75 0 0 0 0 1.5Z" clipRule="evenodd" />
    </Icon>
);