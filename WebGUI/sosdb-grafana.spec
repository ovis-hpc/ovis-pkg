Name:		sosdb-grafana
Version:	4.0.0
Release:	1%{?dist}
Summary:	Grafana plugin for accessing SOS databases

Group:		ovis-ui
License:	Dual GPL/BSD
URL:		http://www.opengridcomputing.com
Source0:	%{name}-%{version}.tar.gz

%define _prefix /var/www/ovis_web_svcs/
%define _gplugins /var/lib/grafana/plugins

# BuildRequires:
Requires:	sosdb-ui >= %{version}

%description
A Grafana data source plugin that implements access to a SOS object store

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%files
%defattr(-,root,root)
%{_gplugins}/sosds/Gruntfile.js
%{_gplugins}/sosds/LICENSE
%{_gplugins}/sosds/README.md
%{_gplugins}/sosds/dist/css/query-editor.css
%{_gplugins}/sosds/dist/datasource.js
%{_gplugins}/sosds/dist/datasource.js.map
%{_gplugins}/sosds/dist/img/ogc_logo.png
%{_gplugins}/sosds/dist/module.js
%{_gplugins}/sosds/dist/module.js.map
%{_gplugins}/sosds/dist/partials/annotations.editor.html
%{_gplugins}/sosds/dist/partials/config.html
%{_gplugins}/sosds/dist/partials/query.editor.html
%{_gplugins}/sosds/dist/partials/query.options.html
%{_gplugins}/sosds/dist/plugin.json
%{_gplugins}/sosds/dist/query_ctrl.js
%{_gplugins}/sosds/dist/query_ctrl.js.map
%{_gplugins}/sosds/package.json
%defattr(-,apache,apache)
%{_prefix}/grafana/__init__.py
%{_prefix}/grafana/__init__.pyc
%{_prefix}/grafana/__init__.pyo
%{_prefix}/grafana/models_baler.py
%{_prefix}/grafana/models_baler.pyc
%{_prefix}/grafana/models_baler.pyo
%{_prefix}/grafana/models_sos.py
%{_prefix}/grafana/models_sos.pyc
%{_prefix}/grafana/models_sos.pyo
%{_prefix}/grafana/urls.py
%{_prefix}/grafana/urls.pyc
%{_prefix}/grafana/urls.pyo
%{_prefix}/grafana/views.py
%{_prefix}/grafana/views.pyc
%{_prefix}/grafana/views.pyo
%{_prefix}/sosgui/grafana_settings.py
%{_prefix}/sosgui/grafana_settings.pyc
%{_prefix}/sosgui/grafana_settings.pyo

%doc

%changelog

