package com.techday.catvision.utility;

import java.time.LocalDate;
import java.time.Period;

public class Utility {
	
	public static boolean checkDateOlderThanDays(LocalDate currentDate, LocalDate newDate, int days) {	
		Period period = Period.between(currentDate, newDate);
		
		if (period.getDays() <= Math.abs(days)) {
			return true;
		}
		
		return false;
	}
	
	public static LocalDate convertToDate(String date) {
		int day = Integer.parseInt((date.substring(6, 8)));
		int month = Integer.parseInt((date.substring(4, 6)));
		int year = Integer.parseInt((date.substring(0, 4)));
		
		return LocalDate.of(year, month, day);
		
	}

}
