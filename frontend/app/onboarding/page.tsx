import ProfileForm from '../../components/ProfileForm';
import CVUploadPanel from '../../components/CVUploadPanel';

export default function OnboardingPage() {
    return (
        <div>
            <h1>Onboarding</h1>
            <ProfileForm />
            <CVUploadPanel />
        </div>
    );
}
