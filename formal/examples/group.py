import formal
from formal.examples import main

class GroupFormPage(main.FormExamplePage):
    
    title = 'Field Group Form'
    description = 'Groups of fields on a form'
    
    def form_example(self, ctx):
        form = formal.Form()

        form.addField('before', formal.String())

        group = formal.Group('group')
        group.add(formal.Field('one', formal.String()))
        group.add(formal.Field('two', formal.String()))
        group.add(formal.Field('pass', formal.String(),
            widgetFactory=formal.CheckedPassword))
        form.add(group)

        form.addField('after', formal.String())

        form.addAction(self.submitted)
        form.data = {
            'before': 'before',
            'group': {
                'one': 'one',
            },
            'after': 'after'
        }
        return form

    def submitted(self, ctx, form, data):
        print form, data
