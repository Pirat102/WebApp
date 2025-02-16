export const initialFilters = {
  operating_mode: "",
  experience: "",
  skills: [],
  location: "",
  scraped_date: "",
  source: "",
};

export const filterSections = [
  {
    id: 'operating_mode',
    titleKey: 'work_mode', // we'll use titleKey instead of title
    defaultOpen: true,
    options: [
      { value: 'Remote', labelKey: 'remote' },
      { value: 'Hybrid', labelKey: 'hybrid' },
      { value: 'Office', labelKey: 'office' },
    ]
  },
  {
    id: 'experience',
    titleKey: 'experience_level',
    defaultOpen: true,
    options: [
      { value: 'Trainee', labelKey: 'trainee' },
      { value: 'Junior', labelKey: 'junior' },
      { value: 'Mid', labelKey: 'mid' },
      { value: 'Senior', labelKey: 'senior' },
      { value: 'Expert', labelKey: 'expert' },
    ]
  },
  {
    id: 'skills',
    titleKey: 'technologies',
    defaultOpen: true,
    isSkillSection: true,
    topSkills: []
  },
  {
    id: 'location',
    titleKey: 'location',
    defaultOpen: false,
    options: [
      { value: 'Warszawa', labelKey: 'warsaw' },
      { value: 'Kraków', labelKey: 'krakow' },
      { value: 'Wrocław', labelKey: 'wroclaw' },
      { value: 'Poznań', labelKey: 'poznan' },
      { value: 'Gdańsk', labelKey: 'gdansk' },
    ]
  },
  {
    id: 'scraped_date',
    titleKey: 'dates_from',
    defaultOpen: false,
    options: []
  },
  {
    id: 'source',
    titleKey: 'source',
    defaultOpen: false,
    options: [
      { value: 'Pracuj.pl', labelKey: 'pracuj_pl' },
      { value: 'NoFluffJobs', labelKey: 'nofluffjobs' },
      { value: 'JustJoinIt', labelKey: 'justjoinit' },
      { value: 'TheProtocol', labelKey: 'theprotocol' },
    ]
  }
];