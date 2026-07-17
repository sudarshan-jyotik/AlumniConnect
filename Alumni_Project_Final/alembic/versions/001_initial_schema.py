"""Initial schema

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-02-12 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create ENUM types first
    user_role_enum = postgresql.ENUM('student', 'alumni', 'admin', name='userrole', create_type=False)
    user_role_enum.create(op.get_bind(), checkfirst=True)
    
    user_status_enum = postgresql.ENUM('pending', 'active', 'suspended', 'inactive', name='userstatus', create_type=False)
    user_status_enum.create(op.get_bind(), checkfirst=True)
    
    request_status_enum = postgresql.ENUM('draft', 'pending', 'approved', 'rejected', 'fulfilled', 'closed', name='requeststatus', create_type=False)
    request_status_enum.create(op.get_bind(), checkfirst=True)
    
    request_priority_enum = postgresql.ENUM('low', 'medium', 'high', 'urgent', name='requestpriority', create_type=False)
    request_priority_enum.create(op.get_bind(), checkfirst=True)
    
    submission_status_enum = postgresql.ENUM('pending', 'approved', 'rejected', 'submitted_to_company', 'interview_scheduled', 'offer_received', 'rejected_by_company', 'withdrawn', name='submissionstatus', create_type=False)
    submission_status_enum.create(op.get_bind(), checkfirst=True)
    
    notification_type_enum = postgresql.ENUM('request_approved', 'request_rejected', 'request_expired', 'new_submission', 'submission_approved', 'submission_rejected', 'new_endorsement', 'interview_scheduled', 'offer_received', 'account_verified', 'welcome', name='notificationtype', create_type=False)
    notification_type_enum.create(op.get_bind(), checkfirst=True)
    
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(length=200), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('role', user_role_enum, nullable=False, server_default='student'),
        sa.Column('status', user_status_enum, nullable=False, server_default='pending'),
        sa.Column('is_email_verified', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('verification_token', sa.String(), nullable=True),
        sa.Column('verification_sent_at', sa.DateTime(), nullable=True),
        sa.Column('verified_at', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('last_login_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('verification_token')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    op.create_index(op.f('ix_users_verification_token'), 'users', ['verification_token'], unique=False)
    
    # Create companies table
    op.create_table(
        'companies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('industry', sa.String(length=100), nullable=True),
        sa.Column('website', sa.String(length=500), nullable=True),
        sa.Column('careers_page', sa.String(length=500), nullable=True),
        sa.Column('logo_url', sa.String(length=500), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('headquarters', sa.String(length=200), nullable=True),
        sa.Column('company_size', sa.String(length=50), nullable=True),
        sa.Column('company_type', sa.String(length=50), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('is_verified', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('request_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_companies_name'), 'companies', ['name'], unique=False)
    
    # Create alumni_profiles table
    op.create_table(
        'alumni_profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('current_company_id', sa.Integer(), nullable=True),
        sa.Column('current_position', sa.String(length=200), nullable=True),
        sa.Column('years_of_experience', sa.Integer(), nullable=True),
        sa.Column('graduation_year', sa.Integer(), nullable=False),
        sa.Column('degree', sa.String(length=100), nullable=True),
        sa.Column('department', sa.String(length=100), nullable=True),
        sa.Column('college_email', sa.String(), nullable=True),
        sa.Column('linkedin_url', sa.String(length=500), nullable=True),
        sa.Column('is_verified', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('verified_at', sa.DateTime(), nullable=True),
        sa.Column('verified_by_id', sa.Integer(), nullable=True),
        sa.Column('verification_notes', sa.Text(), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('expertise_areas', sa.Text(), nullable=True),
        sa.Column('is_available', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('max_requests_per_month', sa.Integer(), nullable=True, server_default='5'),
        sa.Column('current_month_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('referrals_given', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('referrals_successful', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('success_rate', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['current_company_id'], ['companies.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['verified_by_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_alumni_profiles_user_id'), 'alumni_profiles', ['user_id'], unique=False)
    
    # Create referral_requests table
    op.create_table(
        'referral_requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.Column('position_title', sa.String(length=200), nullable=False),
        sa.Column('job_description', sa.Text(), nullable=True),
        sa.Column('job_url', sa.String(length=500), nullable=True),
        sa.Column('location', sa.String(length=200), nullable=True),
        sa.Column('motivation', sa.Text(), nullable=False),
        sa.Column('skills_match', sa.Text(), nullable=True),
        sa.Column('resume_url', sa.String(length=500), nullable=True),
        sa.Column('status', request_status_enum, nullable=False, server_default='draft'),
        sa.Column('priority', request_priority_enum, nullable=True, server_default='medium'),
        sa.Column('tags', sa.Text(), nullable=True),
        sa.Column('admin_notes', sa.Text(), nullable=True),
        sa.Column('approved_by_id', sa.Integer(), nullable=True),
        sa.Column('approved_at', sa.DateTime(), nullable=True),
        sa.Column('rejection_reason', sa.Text(), nullable=True),
        sa.Column('rejected_at', sa.DateTime(), nullable=True),
        sa.Column('application_deadline', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('view_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('endorsement_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('is_urgent', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('is_featured', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['approved_by_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['student_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_referral_requests_company_id'), 'referral_requests', ['company_id'], unique=False)
    op.create_index(op.f('ix_referral_requests_created_at'), 'referral_requests', ['created_at'], unique=False)
    op.create_index(op.f('ix_referral_requests_status'), 'referral_requests', ['status'], unique=False)
    op.create_index(op.f('ix_referral_requests_student_id'), 'referral_requests', ['student_id'], unique=False)
    
    # Create referral_submissions table
    op.create_table(
        'referral_submissions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('request_id', sa.Integer(), nullable=False),
        sa.Column('alumni_id', sa.Integer(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('internal_reference_id', sa.String(length=100), nullable=True),
        sa.Column('confidence_level', sa.Integer(), nullable=True, server_default='3'),
        sa.Column('status', submission_status_enum, nullable=False, server_default='pending'),
        sa.Column('approved_at', sa.DateTime(), nullable=True),
        sa.Column('approved_by_id', sa.Integer(), nullable=True),
        sa.Column('rejection_reason', sa.Text(), nullable=True),
        sa.Column('rejected_at', sa.DateTime(), nullable=True),
        sa.Column('submitted_to_company_at', sa.DateTime(), nullable=True),
        sa.Column('interview_date', sa.DateTime(), nullable=True),
        sa.Column('interview_feedback', sa.Text(), nullable=True),
        sa.Column('outcome_notes', sa.Text(), nullable=True),
        sa.Column('outcome_updated_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['alumni_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['approved_by_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['request_id'], ['referral_requests.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_referral_submissions_alumni_id'), 'referral_submissions', ['alumni_id'], unique=False)
    op.create_index(op.f('ix_referral_submissions_created_at'), 'referral_submissions', ['created_at'], unique=False)
    op.create_index(op.f('ix_referral_submissions_request_id'), 'referral_submissions', ['request_id'], unique=False)
    op.create_index(op.f('ix_referral_submissions_status'), 'referral_submissions', ['status'], unique=False)
    
    # Create endorsements table
    op.create_table(
        'endorsements',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('request_id', sa.Integer(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('strength', sa.Integer(), nullable=True, server_default='3'),
        sa.Column('endorsement_type', sa.String(length=50), nullable=True, server_default='general'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['request_id'], ['referral_requests.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'request_id')
    )
    op.create_index(op.f('ix_endorsements_created_at'), 'endorsements', ['created_at'], unique=False)
    
    # Create notifications table
    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('type', notification_type_enum, nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('action_url', sa.String(length=500), nullable=True),
        sa.Column('action_text', sa.String(length=100), nullable=True),
        sa.Column('entity_type', sa.String(length=50), nullable=True),
        sa.Column('entity_id', sa.Integer(), nullable=True),
        sa.Column('is_read', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('read_at', sa.DateTime(), nullable=True),
        sa.Column('send_email', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('email_sent', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('email_sent_at', sa.DateTime(), nullable=True),
        sa.Column('email_error', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notifications_created_at'), 'notifications', ['created_at'], unique=False)
    op.create_index(op.f('ix_notifications_is_read'), 'notifications', ['is_read'], unique=False)
    op.create_index(op.f('ix_notifications_type'), 'notifications', ['type'], unique=False)
    op.create_index(op.f('ix_notifications_user_id'), 'notifications', ['user_id'], unique=False)
    
    # Create refresh_tokens table
    op.create_table(
        'refresh_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('revoked', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token')
    )
    op.create_index(op.f('ix_refresh_tokens_token'), 'refresh_tokens', ['token'], unique=False)
    op.create_index(op.f('ix_refresh_tokens_user_id'), 'refresh_tokens', ['user_id'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index(op.f('ix_refresh_tokens_user_id'), table_name='refresh_tokens')
    op.drop_index(op.f('ix_refresh_tokens_token'), table_name='refresh_tokens')
    op.drop_table('refresh_tokens')
    
    op.drop_index(op.f('ix_notifications_user_id'), table_name='notifications')
    op.drop_index(op.f('ix_notifications_type'), table_name='notifications')
    op.drop_index(op.f('ix_notifications_is_read'), table_name='notifications')
    op.drop_index(op.f('ix_notifications_created_at'), table_name='notifications')
    op.drop_table('notifications')
    
    op.drop_index(op.f('ix_endorsements_created_at'), table_name='endorsements')
    op.drop_table('endorsements')
    
    op.drop_index(op.f('ix_referral_submissions_status'), table_name='referral_submissions')
    op.drop_index(op.f('ix_referral_submissions_request_id'), table_name='referral_submissions')
    op.drop_index(op.f('ix_referral_submissions_created_at'), table_name='referral_submissions')
    op.drop_index(op.f('ix_referral_submissions_alumni_id'), table_name='referral_submissions')
    op.drop_table('referral_submissions')
    
    op.drop_index(op.f('ix_referral_requests_student_id'), table_name='referral_requests')
    op.drop_index(op.f('ix_referral_requests_status'), table_name='referral_requests')
    op.drop_index(op.f('ix_referral_requests_created_at'), table_name='referral_requests')
    op.drop_index(op.f('ix_referral_requests_company_id'), table_name='referral_requests')
    op.drop_table('referral_requests')
    
    op.drop_index(op.f('ix_alumni_profiles_user_id'), table_name='alumni_profiles')
    op.drop_table('alumni_profiles')
    
    op.drop_index(op.f('ix_companies_name'), table_name='companies')
    op.drop_table('companies')
    
    op.drop_index(op.f('ix_users_verification_token'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    
    # Drop ENUM types
    sa.Enum(name='notificationtype').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='submissionstatus').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='requestpriority').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='requeststatus').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='userstatus').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='userrole').drop(op.get_bind(), checkfirst=True)
