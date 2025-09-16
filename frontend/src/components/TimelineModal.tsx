import type { Component } from 'solid-js';
import type { AIActivity } from '../utils/aiActivities';
import { getActivityIcon, getActivityColor } from '../utils/aiActivities';

interface TimelineModalProps {
  activities: AIActivity[];
  isOpen: boolean;
  onClose: () => void;
}

const TimelineModal: Component<TimelineModalProps> = (props) => {
  return (
    <div class={`modal ${props.isOpen ? 'modal-open' : ''}`}>
      <div class="modal-box w-11/12 max-w-3xl">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-2xl font-bold">AI Activity Timeline</h2>
          <button class="btn btn-sm btn-circle" onClick={props.onClose}>
            ✕
          </button>
        </div>
        
        <div class="space-y-4">
          {props.activities.map((activity) => (
            <div class="flex">
              <div class="flex flex-col items-center mr-4">
                <div class={`w-10 h-10 rounded-full flex items-center justify-center text-white ${getActivityColor(activity.type)}`}>
                  {getActivityIcon(activity.type)}
                </div>
                <div class="h-full w-0.5 bg-base-300"></div>
              </div>
              <div class="flex-grow pb-4">
                <div class="flex justify-between">
                  <h3 class="font-bold">{activity.description}</h3>
                  <span class="text-sm text-base-content/50">
                    {activity.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </span>
                </div>
                {activity.details && (
                  <p class="text-base-content/80 mt-1">{activity.details}</p>
                )}
              </div>
            </div>
          ))}
        </div>
        
        <div class="modal-action">
          <button class="btn" onClick={props.onClose}>Close</button>
        </div>
      </div>
    </div>
  );
};

export default TimelineModal;