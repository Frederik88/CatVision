package com.techday.catvision;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.LocalDate;

import org.junit.jupiter.api.Test;

import com.techday.catvision.utility.Utility;

public class CatvisionUtilityTest {

	
	//@Test
	public void returnTrueIfOlderThanDays() {
		LocalDate currentDate = LocalDate.of(2020, 10, 5);
		LocalDate newDate = LocalDate.of(2020, 10, 10);
		int days = 5;
		
		assertTrue(Utility.checkDateOlderThanDays(currentDate, newDate, days));
	}
	
	//@Test
	public void returnFalseIfEarlierThanDays() {
		LocalDate currentDate = LocalDate.of(2020, 10, 5);
		LocalDate newDate = LocalDate.of(2020, 10, 10);
		int days = 3;
		
		assertFalse(Utility.checkDateOlderThanDays(currentDate, newDate, days));
	}
	
	//@Test
	public void returnTrueIfOlderThanDaysForNegativeDays() {
		LocalDate currentDate = LocalDate.of(2020, 10, 5);
		LocalDate newDate = LocalDate.of(2020, 10, 10);
		int days = -5;
		
		assertTrue(Utility.checkDateOlderThanDays(currentDate, newDate, days));
	}
	
	//@Test
	public void returnValidDateAfterConversion() {
		String date = "20201001-123427";
		LocalDate toConvertTo = LocalDate.of(2020, 10, 01);
		LocalDate convertDate = Utility.convertToDate(date);
		
		assertEquals(toConvertTo, convertDate);
	}
	
}
