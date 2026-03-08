package org.springframework.samples.petclinic.config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.ConstructorBinding;

@ConstructorBinding
@ConfigurationProperties(prefix = "petclinic")
public class AppProperties {

	private final String clinicName;

	private final int maxVisitsPerDay;

	private final boolean enableNotifications;

	public AppProperties(String clinicName, int maxVisitsPerDay, boolean enableNotifications) {
		this.clinicName = clinicName;
		this.maxVisitsPerDay = maxVisitsPerDay;
		this.enableNotifications = enableNotifications;
	}

	public String getClinicName() {
		return clinicName;
	}

	public int getMaxVisitsPerDay() {
		return maxVisitsPerDay;
	}

	public boolean isEnableNotifications() {
		return enableNotifications;
	}

}
