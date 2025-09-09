import { Component, createSignal, createResource, Show, createMemo } from 'solid-js';
import { SkillBankService, type SkillBankResponse } from '../../../../services/SkillBankService';
import SkillsSection from './sections/SkillsSection';
import SummariesSection from './sections/SummariesSection';
import ExperienceSection from './sections/ExperienceSection';
import EducationSection from './sections/EducationSection';
import ProjectsSection from './sections/ProjectsSection';
import CertificationsSection from './sections/CertificationsSection';
import ContactInfoSection from './sections/ContactInfoSection';

interface SkillBankProps {
  userId?: string;
}

const skillBankService = new SkillBankService();

/**
 * Skill Bank Dashboard - Complete Solid.js Version with DaisyUI styling
 * Manages skills, professional summaries, and work experience
 */
const SkillBankDashboard: Component<SkillBankProps> = props => {
  const [activeTab, setActiveTab] = createSignal<
    'contact' | 'skills' | 'summaries' | 'experience' | 'education' | 'projects' | 'certifications'
  >('contact');
  const [refreshTrigger, setRefreshTrigger] = createSignal(0);

  const userId = () => props.userId || 'local-dev-user';

  // Create resource for skill bank data with refresh capability
  const [skillBank] = createResource(
    () => [userId(), refreshTrigger()],
    async ([userId]) => {
      try {
        return await skillBankService.getSkillBank(String(userId));
      } catch (error) {
        console.error('Failed to load skill bank:', error);
        // Return empty skill bank structure on error
        return {
          id: '',
          user_id: String(userId),
          skills: [],
          skill_categories: {},
          default_summary: '',
          summary_variations: [],
          work_experiences: [],
          education_entries: [],
          projects: [],
          certifications: [],
          experience_content_variations: [],
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        } as SkillBankResponse;
      }
    }
  );

  // Computed values for tab counts
  const tabCounts = createMemo(() => {
    const sb = skillBank();
    if (!sb) return {};
    
    return {
      skills: sb.skills?.length || 0,
      summaries: sb.summary_variations?.length || 0,
      experience: sb.work_experiences?.length || 0,
      education: sb.education_entries?.length || 0,
      projects: sb.projects?.length || 0,
      certifications: sb.certifications?.length || 0,
    };
  });

  // Trigger refresh of skill bank data
  const refreshSkillBank = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  // Handle tab change
  const handleTabChange = (
    tab: 'contact' | 'skills' | 'summaries' | 'experience' | 'education' | 'projects' | 'certifications'
  ) => {
    setActiveTab(tab);
  };

  return (
    <div class='container mx-auto p-4'>
      <div class='bg-base-100 rounded-box shadow-lg overflow-hidden'>
        {/* Header */}
        <div class='bg-primary text-primary-content p-6'>
          <div class='flex flex-col md:flex-row md:items-center md:justify-between gap-4'>
            <div>
              <h1 class='text-3xl font-bold'>Skill Bank</h1>
              <p class='opacity-80'>
                Manage your professional skills, experiences, and career assets
              </p>
            </div>
            <div class='flex items-center gap-2'>
              <div class='badge badge-outline badge-lg'>
                {skillBank() ? `${skillBank()?.skills?.length || 0} skills` : 'Loading...'}
              </div>
              <button
                class='btn btn-ghost btn-sm'
                onClick={refreshSkillBank}
                disabled={skillBank.loading}
                title='Refresh data'
              >
                <svg
                  class={`w-4 h-4 ${skillBank.loading ? 'animate-spin' : ''}`}
                  fill='none'
                  stroke='currentColor'
                  viewBox='0 0 24 24'
                >
                  <path
                    stroke-linecap='round'
                    stroke-linejoin='round'
                    stroke-width='2'
                    d='M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15'
                  ></path>
                </svg>
              </button>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div class='border-b border-base-300'>
          <div class='tabs tabs-boxed justify-start p-2'>
            <button
              class={`tab tab-lg gap-2 ${activeTab() === 'contact' ? 'tab-active' : ''}`}
              onClick={() => handleTabChange('contact')}
            >
              <svg class='w-4 h-4' fill='none' stroke='currentColor' viewBox='0 0 24 24'>
                <path
                  stroke-linecap='round'
                  stroke-linejoin='round'
                  stroke-width='2'
                  d='M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z'
                ></path>
              </svg>
              Contact Info
            </button>
            <button
              class={`tab tab-lg gap-2 ${activeTab() === 'skills' ? 'tab-active' : ''}`}
              onClick={() => handleTabChange('skills')}
            >
              <svg class='w-4 h-4' fill='none' stroke='currentColor' viewBox='0 0 24 24'>
                <path
                  stroke-linecap='round'
                  stroke-linejoin='round'
                  stroke-width='2'
                  d='M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 11-7.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z'
                ></path>
              </svg>
              Skills ({tabCounts().skills})
            </button>
            <button
              class={`tab tab-lg gap-2 ${activeTab() === 'summaries' ? 'tab-active' : ''}`}
              onClick={() => handleTabChange('summaries')}
            >
              <svg class='w-4 h-4' fill='none' stroke='currentColor' viewBox='0 0 24 24'>
                <path
                  stroke-linecap='round'
                  stroke-linejoin='round'
                  stroke-width='2'
                  d='M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z'
                ></path>
              </svg>
              Summaries ({tabCounts().summaries})
            </button>
            <button
              class={`tab tab-lg gap-2 ${activeTab() === 'experience' ? 'tab-active' : ''}`}
              onClick={() => handleTabChange('experience')}
            >
              <svg class='w-4 h-4' fill='none' stroke='currentColor' viewBox='0 0 24 24'>
                <path
                  stroke-linecap='round'
                  stroke-linejoin='round'
                  stroke-width='2'
                  d='M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6a2 2 0 01-2 2H6a2 2 0 01-2-2V8a2 2 0 012-2V6z'
                ></path>
              </svg>
              Experience ({tabCounts().experience})
            </button>
            <button
              class={`tab tab-lg gap-2 ${activeTab() === 'education' ? 'tab-active' : ''}`}
              onClick={() => handleTabChange('education')}
            >
              <svg class='w-4 h-4' fill='none' stroke='currentColor' viewBox='0 0 24 24'>
                <path
                  stroke-linecap='round'
                  stroke-linejoin='round'
                  stroke-width='2'
                  d='M12 14l9-5-9-5-9 5 9 5z'
                ></path>
                <path
                  stroke-linecap='round'
                  stroke-linejoin='round'
                  stroke-width='2'
                  d='M12 14l6.16-3.422A12.083 12.083 0 0121 18.782V12M4.84 10.578A12.083 12.083 0 003 12v6.782'
                ></path>
                <path
                  stroke-linecap='round'
                  stroke-linejoin='round'
                  stroke-width='2'
                  d='M12 21v-7'
                ></path>
              </svg>
              Education ({tabCounts().education})
            </button>
            <button
              class={`tab tab-lg gap-2 ${activeTab() === 'projects' ? 'tab-active' : ''}`}
              onClick={() => handleTabChange('projects')}
            >
              <svg class='w-4 h-4' fill='none' stroke='currentColor' viewBox='0 0 24 24'>
                <path
                  stroke-linecap='round'
                  stroke-linejoin='round'
                  stroke-width='2'
                  d='M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10'
                ></path>
              </svg>
              Projects ({tabCounts().projects})
            </button>
            <button
              class={`tab tab-lg gap-2 ${activeTab() === 'certifications' ? 'tab-active' : ''}`}
              onClick={() => handleTabChange('certifications')}
            >
              <svg class='w-4 h-4' fill='none' stroke='currentColor' viewBox='0 0 24 24'>
                <path
                  stroke-linecap='round'
                  stroke-linejoin='round'
                  stroke-width='2'
                  d='M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'
                ></path>
              </svg>
              Certifications ({tabCounts().certifications})
            </button>
          </div>
        </div>

        {/* Tab Content */}
        <div class='p-4 min-h-[500px]'>
          <Show when={skillBank.loading}>
            <div class='flex items-center justify-center h-64'>
              <div class='text-center'>
                <div class='loading loading-spinner loading-lg text-primary'></div>
                <p class='mt-2 text-base-content/70'>Loading skill bank...</p>
              </div>
            </div>
          </Show>

          <Show when={skillBank.error}>
            <div class='alert alert-error'>
              <svg class='w-6 h-6' fill='none' stroke='currentColor' viewBox='0 0 24 24'>
                <path
                  stroke-linecap='round'
                  stroke-linejoin='round'
                  stroke-width='2'
                  d='M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z'
                ></path>
              </svg>
              <span>
                Failed to load skill bank data. Please try again later.
              </span>
              <button class='btn btn-sm' onClick={refreshSkillBank}>
                Retry
              </button>
            </div>
          </Show>

          <Show when={!skillBank.loading && !skillBank.error && skillBank()}>
            <Show when={activeTab() === 'contact'}>
              <ContactInfoSection
                skillBank={skillBank()!}
                onUpdate={refreshSkillBank}
                loading={false}
              />
            </Show>

            <Show when={activeTab() === 'skills'}>
              <SkillsSection
                skillBank={skillBank()!}
                onUpdate={refreshSkillBank}
                loading={false}
              />
            </Show>

            <Show when={activeTab() === 'summaries'}>
              <SummariesSection
                skillBank={skillBank()!}
                onUpdate={refreshSkillBank}
                loading={false}
              />
            </Show>

            <Show when={activeTab() === 'experience'}>
              <ExperienceSection
                skillBank={skillBank()!}
                onUpdate={refreshSkillBank}
                loading={false}
              />
            </Show>

            <Show when={activeTab() === 'education'}>
              <EducationSection
                skillBank={skillBank()!}
                onUpdate={refreshSkillBank}
                loading={false}
              />
            </Show>

            <Show when={activeTab() === 'projects'}>
              <ProjectsSection
                skillBank={skillBank()!}
                onUpdate={refreshSkillBank}
                loading={false}
              />
            </Show>

            <Show when={activeTab() === 'certifications'}>
              <CertificationsSection
                skillBank={skillBank()!}
                onUpdate={refreshSkillBank}
                loading={false}
              />
            </Show>
          </Show>
        </div>
      </div>
    </div>
  );
};

export default SkillBankDashboard;
