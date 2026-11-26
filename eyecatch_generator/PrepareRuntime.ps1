param(
    [Parameter(Mandatory = $true)]
    [string]$OutputDirectory,
    [string]$TemplateZip = (Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'Visual Studio 2022\Templates\ProjectTemplates\OpenSiv3D_0.6.16.zip')
)

$ErrorActionPreference = 'Stop'
$outputRoot = [IO.Path]::GetFullPath($OutputDirectory)
$stamp = Join-Path $outputRoot '.siv3d-0.6.16-runtime'
if ((Test-Path -LiteralPath $stamp -PathType Leaf) -and
    (Test-Path -LiteralPath (Join-Path $outputRoot 'Resource.rc') -PathType Leaf)) {
    return
}

if (!(Test-Path -LiteralPath $TemplateZip -PathType Leaf)) {
    throw "OpenSiv3D template zip not found: $TemplateZip. Set the MSBuild property Siv3DTemplateZip to its path."
}

Add-Type -AssemblyName System.IO.Compression.FileSystem
$archive = [IO.Compression.ZipFile]::OpenRead($TemplateZip)
try {
    $entries = $archive.Entries | Where-Object {
        $_.Name -and ($_.FullName -match '^App/engine/' -or $_.FullName -in @('App/Resource.rc', 'App/icon.ico'))
    }
    if (!($entries.FullName -contains 'App/Resource.rc') -or !($entries.FullName -contains 'App/engine/shader/d3d11/sprite.vs')) {
        throw "The zip does not contain the OpenSiv3D engine assets: $TemplateZip"
    }

    $outputPrefix = $outputRoot.TrimEnd('\') + '\'
    foreach ($entry in $entries) {
        $target = [IO.Path]::GetFullPath((Join-Path $outputRoot $entry.FullName.Substring(4)))
        if (!$target.StartsWith($outputPrefix, [StringComparison]::OrdinalIgnoreCase)) {
            throw "Unexpected path in the OpenSiv3D template: $($entry.FullName)"
        }
        [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($target)) | Out-Null
        [IO.Compression.ZipFileExtensions]::ExtractToFile($entry, $target, $true)
    }
    New-Item -ItemType File -Force -Path $stamp | Out-Null
} finally {
    $archive.Dispose()
}
