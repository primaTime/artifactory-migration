# Articatory migration to GitHub packages

## Getting started

The script is tested in Python version 3.9, make sure you run it in this version or newer (newer version may have some problems). The script uses the requests and dateutil package, which you install using pip (`pip install requests`).
You also need to have maven installed on your computer to run the script. And the `mvn` command in the terminal must work.

You also need to set up maven settings on your computer. Below is a sample settings.xml file, which on macOS is located in ~/.m2/settings.xml.
You need to set up an active profile on github. Then a github server where you type your username into GitHub and a personal access token in place of your password. Then add the GitHub profile with the address to the primaTime repository.

```xml
<?xml version="1.0" encoding="UTF-8"?>

<settings xmlns="http://maven.apache.org/SETTINGS/1.2.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.2.0 http://maven.apache.org/xsd/settings-1.2.0.xsd">
  <pluginGroups>

  </pluginGroups>

  <proxies>

  </proxies>

  <activeProfiles>
    <activeProfile>github</activeProfile>
  </activeProfiles>

  <servers>
    <server>
      <id>github</id>
      <username><!-- USERNAME --></username>
      <password><!-- TOKEN --></password>
    </server>
  </servers>

  <mirrors>
  </mirrors>

  <profiles>
    <profile>
      <id>github</id>
      <repositories>
        <repository>
          <id>central</id>
          <url>https://repo1.maven.org/maven2</url>
        </repository>
        <repository>
          <id>github</id>
          <url>https://maven.pkg.github.com/primaTime/api</url>
          <snapshots>
            <enabled>true</enabled>
          </snapshots>
        </repository>
      </repositories>
    </profile>
  </profiles>

</settings>
```

If you use the --help argument, you will learn which arguments need to be set and what they are for.