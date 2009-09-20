from Products.ImageEditor.tests.base import ImageEditorTestCase
from Products.CMFCore.utils import getToolByName
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from zope.component import getUtility
from Products.ImageEditor.Extensions import Install

class TestSetup(ImageEditorTestCase):
    """Test if install of the product is well done"""
    
    def test_css_registry(self):
        pcss = self.portal.portal_css
#        self.failUnless('++resource++imageeditor-style.css' in [css.getId() for css in pcss.getResources()])

    def test_actions(self):
        actionTool = self.portal.portal_actions
        actionInfo = actionTool.getActionInfo(['object/image_editor'])
        self.failUnless(actionInfo['url'] == "/@@imageeditor")

    def test_js_added(self):
        pjavascripts = getToolByName(self.portal, 'portal_javascripts')
        self.failUnless('++resource++jquery.imgareaselect-0.8.min.js' in [js.getId() for js in pjavascripts.getResources()])

    def test_should_install_collective_js_jqueryui(self):
        qi = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(qi.isProductInstalled('collective.js.jqueryui'))

    def test_should_remove_stack_pos_on_uninstall(self):
        image = self.getImageContentType()
        image.stack_pos = 5
        self.uninstall()
        self.assertEquals(hasattr(image, 'stack_pos'), False)
        
    def test_should_remove_unredostack_on_uninstall(self):
        image = self.getImageContentType()
        image.unredostack = 5
        self.uninstall()
        self.assertEquals(hasattr(image, 'unredostack'), False)
        
    def test_should_remove_css_on_uninstall(self):
        self.uninstall()
        pcss = self.portal.portal_css
#        self.failUnless('++resource++imageeditor-style.css' not in [css.getId() for css in pcss.getResources()])
        
    def test_should_remove_action_object_on_uninstall(self):
        self.uninstall()
        actionTool = self.portal.portal_actions
        object_actions = actionTool.object
        self.assertEquals('image_editor' in object_actions.objectIds(), False)
        
    def test_should_remove_javascript_on_uninstall(self):
        self.uninstall()
        pjavascripts = getToolByName(self.portal, 'portal_javascripts')
        jsresources = [js.getId() for js in pjavascripts.getResources()]
        self.failUnless('++resource++jquery.imgareaselect-0.8.min.js' not in jsresources)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSetup))
    return suite
