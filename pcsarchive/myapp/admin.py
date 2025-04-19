from django.contrib import admin
from .models import Entity, Class, Site, User, SecurityClearance, Personnel
# Register your models here.

# For Class model
class ClassAdmin(admin.ModelAdmin):
    list_display = ('class_id', 'class_name')  # Shows class_id and class_name
admin.site.register(Class, ClassAdmin)

# For Site model
class SiteAdmin(admin.ModelAdmin):
    list_display = ('siteid', 'name', 'address')  # Shows siteid, name, and address
admin.site.register(Site, SiteAdmin)

# For Entity model
class EntityAdmin(admin.ModelAdmin):
    list_display = ('eid', 'name', 'location', 'class_ref', 'description')  # Shows eid, name, location, class_ref, description
admin.site.register(Entity, EntityAdmin)

# For SecurityClearance model
class SecurityClearanceAdmin(admin.ModelAdmin):
    list_display = ('scid', 'level')  # Shows scid and level
admin.site.register(SecurityClearance, SecurityClearanceAdmin)

# For Personnel model
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ('pid', 'name', 'location', 'clearance')  # Shows pid, name, location, and clearance
admin.site.register(Personnel, PersonnelAdmin)

# For User model
class UserAdmin(admin.ModelAdmin):
    list_display = ('uid', 'username', 'email', 'clearance')  # Shows uid, username, email, and clearance
admin.site.register(User, UserAdmin)