PROJECT_STATUS_CHOICES = (
    ('requested', 'Requested'),
    ('scoping', 'Scoping'),
    ('in progress', 'In Progress'),
    ('complete', 'Complete')
)

ACTION_ITEM_STATUS_CHOICES = (
    ('queued', 'Queued'),
    ('scoped', 'Scoped'),
    ('in progress', 'In Progress'),
    ('blocked', 'Blocked'),
    ('validating', 'Validating'),
    ('complete', 'Complete')
)

STAKEHOLDER_TYPE_CHOICES = (
    ('user', 'User'),
    ('governance', 'Governance'),
    ('influencer', 'Influencer'),
    ('provider', 'Provider')
)

DOCUMENT_TYPE_CHOICES = (
    ('notes', 'Note'),
    ('minutes', 'Minutes'),
    ('scoping', 'Scoping')
)

CONTRIBUTOR_TYPE_CHOICES = (
    ('leader', 'Leader'),
    ('team member', 'Team Member'),
    ('contributor', 'Contributor')
)

DISCUSSION_TYPE_CHOICES = (
    ('scoping', 'Scoping'),
    ('update', 'Update'),
    ('presentation', 'Presentation'),
    ('debrief', 'Debrief')
)

TASK_TYPE_CHOICES = (
    ('requirement', 'Requirement'),
    ('nice to have', 'Nice to Have'),
    ('blocker', 'Blocker')
)
