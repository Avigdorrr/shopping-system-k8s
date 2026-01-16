{{/*
Expand the name of the chart.
*/}}
{{- define "shopping-system.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "shopping-system.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}


{{/* Fullname suffixed with -management-api */}}
{{- define "shopping-system.management-api.fullname" -}}
{{- if .Values.managementApi.fullnameOverride -}}
{{- .Values.managementApi.fullnameOverride | trunc 35 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-management-api" (include "shopping-system.fullname" .) -}}
{{- end }}
{{- end }}

{{/* Fullname suffixed with -web-server */}}
{{- define "shopping-system.web-server.fullname" -}}
{{- if .Values.webServer.fullnameOverride -}}
{{- .Values.webServer.fullnameOverride | trunc 35 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-web-server" (include "shopping-system.fullname" .) -}}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "shopping-system.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "shopping-system.labels" -}}
helm.sh/chart: {{ include "shopping-system.chart" . }}
app.kubernetes.io/name: {{ include "shopping-system.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels for Management API
*/}}
{{- define "shopping-system.management-api.selectorLabels" -}}
app.kubernetes.io/name: {{ include "shopping-system.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: management-api
{{- end }}

{{/*
Selector labels for Web Server
*/}}
{{- define "shopping-system.web-server.selectorLabels" -}}
app.kubernetes.io/name: {{ include "shopping-system.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: web-server
{{- end }}

{{/*
Create the name of the service account for Management API
*/}}
{{- define "shopping-system.management-api.serviceAccountName" -}}
{{- if .Values.managementApi.serviceAccount.create }}
{{- default (include "shopping-system.management-api.fullname" .) .Values.managementApi.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.managementApi.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Create the name of the service account for Web Server
*/}}
{{- define "shopping-system.web-server.serviceAccountName" -}}
{{- if .Values.webServer.serviceAccount.create }}
{{- default (include "shopping-system.web-server.fullname" .) .Values.webServer.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.webServer.serviceAccount.name }}
{{- end }}
{{- end }}