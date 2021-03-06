from .auth.register import register_user
from .home import home
from .connection import Connection

from .job.list import job_list
from .job.form import job_form
from .job.detail import job_details_form

from .response.list import response_list
from .response.form import response_form, response_edit_form
from .response.detail import response_details_form

from .resource.list import resource_list
from .resource.detail import resource_detail_form
from .resource.form import resource_form, resource_edit_form

from .auth.logout import logout_user