class PackageManagerProxy(object):
	def __init__(self):
		# do nothing, but initialize placeholders for instance variables
		self.registry = None
		self.cache_dir = None
		self.isolate_pkg_info = False
		self.metadata_format = None
		self.dep_format = None
		self.name = 'pypi'

	def get_metadata(self, pkg_name, pkg_version=None):
		# load the metadata information for a package or get and cache it in cache_dir
		pass

	def get_versions(self, pkg_name, max_num=15, min_gap_days=30, with_time=False):
		# read the metadata and get (major) versions of the specified package
		pass

	def parse_deps_file(self, deps_file):
		# parse dependencies list in a file
		pass

	def get_author(self, pkg_name):
		# read the metadata and get author name and email of the specified package
		pass

	def get_version_hash(self, pkg_name, pkg_version, algorithm='sha1'):
		# get the hash of the package version
		pass
