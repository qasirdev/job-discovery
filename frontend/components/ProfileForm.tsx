'use client';

import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { TextField, Button, Box, Typography } from '@mui/material';

const profileSchema = z.object({
  full_name: z.string().min(1, 'Full name is required'),
  email: z.string().email('Invalid email address'),
  target_role: z.string().min(1, 'Target role is required'),
  target_location: z.string().min(1, 'Target location is required'),
  skills: z.string().min(1, 'Skills are required'),
  years_experience: z.coerce.number().min(0, 'Years of experience must be 0 or more'),
});

export type ProfileFormData = z.infer<typeof profileSchema>;

export interface UserProfile extends ProfileFormData {
  id: string;
  cv_filename?: string;
}

interface ProfileFormProps {
  onSubmit: (data: ProfileFormData) => Promise<void>;
  initialData?: UserProfile;
}

export default function ProfileForm({ onSubmit, initialData }: ProfileFormProps) {
  const {
    control,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      full_name: initialData?.full_name || '',
      email: initialData?.email || '',
      target_role: initialData?.target_role || '',
      target_location: initialData?.target_location || '',
      skills: initialData?.skills || '',
      years_experience: initialData?.years_experience || 0,
    },
  });

  const [formError, setFormError] = React.useState<string | null>(null);

  const onSubmitHandler = async (data: ProfileFormData) => {
    setFormError(null);
    try {
      await onSubmit(data);
    } catch (err: any) {
      setFormError(err.message || 'Failed to submit profile');
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit(onSubmitHandler)} className="flex flex-col gap-4 max-w-md bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <Typography variant="h6" className="mb-2">Your Profile</Typography>

      <Controller
        name="full_name"
        control={control}
        render={({ field }) => (
          <TextField
            {...field}
            label="Full Name"
            error={!!errors.full_name}
            helperText={errors.full_name?.message}
            fullWidth
            size="small"
          />
        )}
      />

      <Controller
        name="email"
        control={control}
        render={({ field }) => (
          <TextField
            {...field}
            label="Email"
            type="email"
            error={!!errors.email}
            helperText={errors.email?.message}
            fullWidth
            size="small"
          />
        )}
      />

      <Controller
        name="target_role"
        control={control}
        render={({ field }) => (
          <TextField
            {...field}
            label="Target Role"
            error={!!errors.target_role}
            helperText={errors.target_role?.message}
            fullWidth
            size="small"
          />
        )}
      />

      <Controller
        name="target_location"
        control={control}
        render={({ field }) => (
          <TextField
            {...field}
            label="Target Location"
            error={!!errors.target_location}
            helperText={errors.target_location?.message}
            fullWidth
            size="small"
          />
        )}
      />

      <Controller
        name="skills"
        control={control}
        render={({ field }) => (
          <TextField
            {...field}
            label="Skills (comma-separated)"
            error={!!errors.skills}
            helperText={errors.skills?.message}
            fullWidth
            size="small"
          />
        )}
      />

      <Controller
        name="years_experience"
        control={control}
        render={({ field }) => (
          <TextField
            {...field}
            label="Years of Experience"
            type="number"
            error={!!errors.years_experience}
            helperText={errors.years_experience?.message}
            fullWidth
            size="small"
          />
        )}
      />

      {formError && (
        <Typography color="error" variant="body2" className="mt-2">
          {formError}
        </Typography>
      )}

      <Button
        type="submit"
        variant="contained"
        color="primary"
        disabled={isSubmitting}
        className="mt-4"
      >
        {isSubmitting ? 'Saving...' : 'Save Profile'}
      </Button>
    </Box>
  );
}
