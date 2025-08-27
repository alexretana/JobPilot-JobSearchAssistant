# UserProfile Components Update Plan

## Development Instructions for UserProfile Components

1. **Analyze the component** - Understand what data it needs and what operations it performs
2. **Update import statements** - Replace `userProfileApi` imports with `UserProfileService`
3. **Instantiate the service** - Create an instance of `UserProfileService`
4. **Update function calls** - Adapt all calls to match the new service interface
5. **Update TypeScript types** - Ensure type compatibility with new service definitions
6. **Test with mock data** - Verify the component works correctly with the new service
7. **Update error/loading states** - Ensure proper handling of async operations

## Component-by-Component Update Process

### ProfileDashboard.tsx

#### Current State Analysis
- Imports `userProfileApi` from `'../../../../services/userProfileApi'`
- Uses `userProfileApi.getProfile()`, `userProfileApi.getDefaultProfile()`, `userProfileApi.calculateCompleteness()`
- Uses `userProfileApi.formatSalaryRange()`

#### Update Steps
1. Replace import:
   ```typescript
   // OLD
   import { userProfileApi, UserProfile, ProfileCompleteness } from '../../../../services/userProfileApi';
   
   // NEW
   import { UserProfileService, UserProfile } from '../../../../services/UserProfileService';
   import type { ProfileCompleteness } from './ProfileCompleteness'; // Local type
   ```

2. Instantiate service:
   ```typescript
   const userProfileService = new UserProfileService();
   ```

3. Update resource function:
   ```typescript
   // OLD
   const [profile, { refetch: refetchProfile }] = createResource(async () => {
     try {
       let userProfile: UserProfile;
       if (props.userId) {
         userProfile = await userProfileApi.getProfile(props.userId);
       } else {
         userProfile = await userProfileApi.getDefaultProfile();
       }
       const completeness = userProfileApi.calculateCompleteness(userProfile);
       setCompletenessData(completeness);
       return userProfile;
     } catch (error) {
       console.error('Error fetching profile:', error);
       throw error;
     }
   });
   
   // NEW
   const [profile, { refetch: refetchProfile }] = createResource(async () => {
     try {
       let userProfile: UserProfile;
       if (props.userId) {
         userProfile = await userProfileService.getProfile(props.userId);
       } else {
         userProfile = await userProfileService.getDefaultProfile();
       }
       // Note: calculateCompleteness needs to be implemented locally or in service
       const completeness = calculateCompletenessLocally(userProfile);
       setCompletenessData(completeness);
       return userProfile;
     } catch (error) {
       console.error('Error fetching profile:', error);
       throw error;
     }
   });
   ```

4. Update utility function calls:
   ```typescript
   // OLD
   {userProfileApi.formatSalaryRange(profile()?.desired_salary_min, profile()?.desired_salary_max)}
   
   // NEW
   {formatSalaryRange(profile()?.desired_salary_min, profile()?.desired_salary_max)}
   ```

#### TypeScript Type Updates
- Ensure all UserProfile types match the new UserProfileService interface
- Update any custom types to align with the new service

#### Testing
- Verify profile loading works with both specific userId and default profile
- Test error states display correctly
- Confirm loading states show during API calls
- Check that profile completeness calculation still works

### ProfileEditForm.tsx

#### Current State Analysis
- Imports `userProfileApi` from `'../../../../services/userProfileApi'`
- Uses `userProfileApi.validateProfile()`, `userProfileApi.updateProfile()`, `userProfileApi.createProfile()`
- Uses `userProfileApi.getJobTypes()`, `userProfileApi.getRemoteTypes()`

#### Update Steps
1. Replace import:
   ```typescript
   // OLD
   import { userProfileApi, UserProfileUpdate } from '../../../../services/userProfileApi';
   
   // NEW
   import { UserProfileService } from '../../../../services/UserProfileService';
   import type { UserProfileUpdate } from '../../../../services/UserProfileService';
   ```

2. Instantiate service:
   ```typescript
   const userProfileService = new UserProfileService();
   ```

3. Update save function:
   ```typescript
   // OLD
   const validationErrors = userProfileApi.validateProfile(formData);
   // ...validation logic...
   if (props.profile?.id) {
     savedProfile = await userProfileApi.updateProfile(props.profile.id, updates);
   } else {
     savedProfile = await userProfileApi.createProfile(formData);
   }
   
   // NEW
   // TODO: Implement validation locally or add to UserProfileService
   const validationErrors = validateProfileLocally(formData);
   // ...validation logic...
   if (props.profile?.id) {
     savedProfile = await userProfileService.updateProfile(props.profile.id, updates);
   } else {
     savedProfile = await userProfileService.createProfile(formData as any); // Type assertion may be needed
   }
   ```

4. Update static data functions:
   ```typescript
   // OLD
   <For each={userProfileApi.getJobTypes()}>
   <For each={userProfileApi.getRemoteTypes()}>
   
   // NEW
   // TODO: Implement these as static functions or import from service
   <For each={getJobTypes()}>
   <For each={getRemoteTypes()}>
   ```

#### TypeScript Type Updates
- Ensure all UserProfileUpdate types match the new UserProfileService interface
- Update any custom types to align with the new service

#### Testing
- Verify profile creation works correctly
- Test profile updates with various field combinations
- Check validation errors display properly
- Confirm job types and remote types populate correctly

### ProfileEditModal.tsx

#### Current State Analysis
- Imports `UserProfile` from `'../../../../services/userProfileApi'`
- Mainly a wrapper component, passes data to ProfileEditForm

#### Update Steps
- Minimal changes needed, mostly relies on ProfileEditForm updates
- Verify type imports are correct

### ProfileCompleteness.tsx

#### Current State Analysis
- Imports `ProfileCompleteness` from `'../../../../services/userProfileApi'`
- Pure presentational component, no API calls

#### Update Steps
- Update import to use local or shared type definition
- No functional changes needed

### ContactInfoSection.tsx

#### Current State Analysis
- Imports `userProfileApi` and `UserProfileUpdate` from `'../../../../services/userProfileApi'`
- Uses `userProfileApi.getProfile()` and `userProfileApi.updateProfile()`

#### Update Steps
1. Replace imports:
   ```typescript
   // OLD
   import { userProfileApi } from '../../../../../services/userProfileApi';
   import type { UserProfileUpdate } from '../../../../../services/userProfileApi';
   
   // NEW
   import { UserProfileService } from '../../../../../services/UserProfileService';
   import type { UserProfileUpdate } from '../../../../../services/UserProfileService';
   ```

2. Instantiate service:
   ```typescript
   const userProfileService = new UserProfileService();
   ```

3. Update API calls:
   ```typescript
   // OLD
   return await userProfileApi.getProfile(userId);
   // ...
   await userProfileApi.updateProfile(userId, updateData);
   
   // NEW
   return await userProfileService.getProfile(userId);
   // ...
   await userProfileService.updateProfile(userId, updateData);
   ```

## Service Implementation Notes

### Missing Functionality
Some functions from the legacy `userProfileApi` need to be reimplemented:

1. `calculateCompleteness()` - Move to a utility function or add to UserProfileService
2. `formatSalaryRange()` - Move to a utility function
3. `validateProfile()` - Move to a utility function or add to UserProfileService
4. `getJobTypes()` - Move to a utility function or add to UserProfileService
5. `getRemoteTypes()` - Move to a utility function or add to UserProfileService

### New Utility Functions Needed
Create these utility functions to replace the missing functionality:

```typescript
// utils/profileUtils.ts
import type { UserProfile } from '../services/UserProfileService';

export const calculateCompleteness = (profile: UserProfile): any => {
  // Implementation based on previous logic
};

export const formatSalaryRange = (min?: number, max?: number): string => {
  // Implementation based on previous logic
};

export const validateProfile = (profile: any): string[] => {
  // Implementation based on previous logic
};

export const getJobTypes = (): string[] => {
  // Return job types array
};

export const getRemoteTypes = (): string[] => {
  // Return remote types array
};
```

## Testing Strategy

### Unit Testing
- Test each utility function independently
- Verify service instantiation works correctly
- Check error handling paths

### Integration Testing
- Test complete component flows with mock service responses
- Verify data flows correctly between components and services
- Check that UI updates properly based on service responses

### Manual Testing
- Test all user interactions (edit, save, cancel)
- Verify loading states display correctly
- Confirm error messages are helpful
- Check responsive design on different screen sizes

This plan provides a systematic approach to updating the UserProfile components to work with the new service layer while maintaining functionality and user experience.