package org.springframework.samples.petclinic;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class PetClinicIntegrationTests {

	@Autowired
	private PetClinicApplication application;

	@Test
	void contextLoads() {
	}

}
