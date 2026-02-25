{{/*
Expand the name of the chart.
*/}}
{{- define "mcp-proto-okn.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "mcp-proto-okn.fullname" -}}
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

{{/*
Create chart label.
*/}}
{{- define "mcp-proto-okn.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels.
*/}}
{{- define "mcp-proto-okn.labels" -}}
helm.sh/chart: {{ include "mcp-proto-okn.chart" . }}
{{ include "mcp-proto-okn.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels.
*/}}
{{- define "mcp-proto-okn.selectorLabels" -}}
app.kubernetes.io/name: {{ include "mcp-proto-okn.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
ServiceAccount name.
*/}}
{{- define "mcp-proto-okn.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "mcp-proto-okn.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Container image reference.
*/}}
{{- define "mcp-proto-okn.image" -}}
{{- $tag := .Values.image.tag | default .Chart.AppVersion }}
{{- printf "%s:%s" .Values.image.repository $tag }}
{{- end }}

{{/*
Determine the ENTRYPOINT command based on serverMode.
*/}}
{{- define "mcp-proto-okn.command" -}}
{{- if eq .Values.serverMode "unified" }}
- mcp-proto-okn-unified
{{- else }}
- mcp-proto-okn
{{- end }}
{{- end }}

{{/*
Name of the generated Secret for the SPARQL endpoint / API key.
*/}}
{{- define "mcp-proto-okn.secretName" -}}
{{- printf "%s-credentials" (include "mcp-proto-okn.fullname" .) }}
{{- end }}
