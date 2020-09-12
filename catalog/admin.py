from django.contrib import admin

# Register your models here.
from catalog.models import *

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

admin.site.register(Author, AuthorAdmin)

class BooksInstanceInLine(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInLine]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('status', 'due_back')

    fieldsets = (
        (
            None, {
                'fields': ('book', 'imprint', 'id')
            }
        ),
        (
            'Availability: ', {
                'fields': ('status', 'due_back')
            }
        )
    )

admin.site.register(Genre)

