import { test as base } from '@playwright/test';
import { mockUserProfile, mockJob, mockSkillBank } from '../utils/mockData';

// Declare the types of your fixtures.
type UserProfileFixture = {
  mockUserProfile: typeof mockUserProfile;
  mockJob: typeof mockJob;
  mockSkillBank: typeof mockSkillBank;
};

// Extend base test by providing the "userProfile" fixture.
export const test = base.extend<UserProfileFixture>({
  mockUserProfile: async ({}, use) => {
    // Set up the fixture
    await use(mockUserProfile);
  },
  
  mockJob: async ({}, use) => {
    // Set up the fixture
    await use(mockJob);
  },
  
  mockSkillBank: async ({}, use) => {
    // Set up the fixture
    await use(mockSkillBank);
  },
});

export { expect } from '@playwright/test';