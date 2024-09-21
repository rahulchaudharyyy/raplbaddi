import os
import importlib
import frappe

__version__ = '0.0.1'
patches_loaded = False
app_name = "raplbaddi"

def load_monkey_patches():
	"""
	Loads all modules present in monkey_patches to override some logic
	in Frappe / ERPNext. Returns if patches have already been loaded earlier.
	"""
	global patches_loaded

	if patches_loaded:
		return

	patches_loaded = True

	if app_name not in frappe.get_installed_apps():
		return

	for module_name in os.listdir(frappe.get_app_path(app_name, "monkey_patches")):
		if not module_name.endswith(".py") or module_name == "__init__.py":
			continue

		importlib.import_module(app_name + ".monkey_patches." + module_name[:-3])

_get_hooks = frappe.get_hooks
def get_hooks(*args, **kwargs):
	load_monkey_patches()
	return _get_hooks(*args, **kwargs)
frappe.get_hooks = get_hooks

_connect = frappe.connect
def connect(*args, **kwargs):
	"""
	Patches frappe.connect to load monkey patches once a connection is
	established with the database.
	"""
	_connect(*args, **kwargs)
	load_monkey_patches()
frappe.connect = connect