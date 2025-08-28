// Example of how to update a component to use the new service layer
// This is a simplified example showing the pattern to follow

import { Component, createSignal, createResource, Show, For } from 'solid-js';
import { UserProfileService, type UserProfile } from '../services/UserProfileService';
import { calculateProfileCompleteness, formatSalaryRange } from '../utils/componentUtils';

// Example component update pattern
const ExampleProfileDashboard: Component = () => {
  // Instantiate the service
  const userProfileService = new UserProfileService();
  
  // State management
  const [showEditModal, setShowEditModal] = createSignal(false);
  
  // Fetch user profile using createResource
  const [profile, { refetch: refetchProfile }] = createResource(async () => {
    try {
      // Use the new service to get the profile
      const userProfile = await userProfileService.getDefaultProfile();
      return userProfile;
    } catch (error) {
      console.error('Error fetching profile:', error);
      throw error;
    }
  });

  // Handler functions
  const handleEditProfile = () => {
    setShowEditModal(true);
  };

  const handleProfileUpdate = async (updatedProfile: UserProfile) => {
    // Refresh the profile data
    refetchProfile();
    setShowEditModal(false);
  };

  return (
    <div class='container mx-auto p-4'>
      {/* Loading State */}
      <Show when={profile.loading}>
        <div class='flex justify-center items-center py-12'>
          <span class='loading loading-spinner loading-lg'></span>
        </div>
      </Show>

      {/* Error State */}
      <Show when={profile.error}>
        <div class='alert alert-error mb-6'>
          <svg class='stroke-current shrink-0 h-6 w-6' fill='none' viewBox='0 0 24 24'>
            <path
              stroke-linecap='round'
              stroke-linejoin='round'
              stroke-width='2'
              d='M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z'
            />
          </svg>
          <span>Error loading profile: {profile.error.message}</span>
          <div>
            <button class='btn btn-sm btn-outline' onClick={() => refetchProfile()}>
              Retry
            </button>
          </div>
        </div>
      </Show>

      {/* Profile Content */}
      <Show when={profile() && !profile.loading}>
        <div class='card bg-base-100 shadow-xl'>
          <div class='card-body'>
            <div class='flex justify-between items-center mb-4'>
              <h2 class='card-title'>Profile Dashboard</h2>
              <button class='btn btn-primary' onClick={handleEditProfile}>
                Edit Profile
              </button>
            </div>
            
            <div class='space-y-4'>
              <div>
                <div class='text-sm font-medium text-base-content/70'>Full Name</div>
                <div class='text-lg'>
                  {[profile()?.first_name, profile()?.last_name].filter(Boolean).join(' ') ||
                    'Not provided'}
                </div>
              </div>
              
              <div>
                <div class='text-sm font-medium text-base-content/70'>Email</div>
                <div class='text-base'>{profile()?.email || 'Not provided'}</div>
              </div>
              
              <div>
                <div class='text-sm font-medium text-base-content/70'>Salary Range</div>
                <div class='text-base'>
                  {formatSalaryRange(profile()?.desired_salary_min, profile()?.desired_salary_max)}
                </div>
              </div>
            </div>
          </div>
        </div>
      </Show>
    </div>
  );
};

export default ExampleProfileDashboard;